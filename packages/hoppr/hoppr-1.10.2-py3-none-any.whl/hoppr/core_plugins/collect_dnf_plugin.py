"""
Collector plugin for DNF packages
"""
from __future__ import annotations

import fnmatch
import os
import shutil
import time

from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote_plus, urlparse

import requests

from pydantic import SecretStr
from requests.auth import HTTPBasicAuth

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import BatchCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_process, hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models import HopprContext
from hoppr.models.credentials import Credentials
from hoppr.models.sbom import Component
from hoppr.models.types import PurlType, RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL


def _artifact_string(purl: PackageURL) -> str:
    arch = purl.qualifiers.get("arch")
    return f"{purl.name}{f'-{purl.version}' if purl.version else ''}{f'.{arch}' if arch else ''}"


def _is_rpm_repo(repo_url: str) -> bool:
    url = RepositoryUrl(url=repo_url) / "repodata/repomd.xml"
    basic_auth = None
    creds = Credentials.find(repo_url)
    if creds is not None and isinstance(creds.password, SecretStr):
        basic_auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())
    for attempt in range(3):
        if attempt > 0:
            time.sleep(5)

        resp = requests.get(f"{url}", auth=basic_auth, allow_redirects=False, stream=True, verify=True, timeout=60)
        if resp.status_code < 300:
            return True
        if resp.status_code < 500:
            return False

    return False


def _repo_proxy(url: str) -> str:
    proxy = os.getenv("https_proxy", "_none_")
    no_proxy_urls = [item for item in os.getenv("no_proxy", "").split(",") if item != ""]

    parsed_url = urlparse(url)

    for pattern in no_proxy_urls:
        if pattern in parsed_url.netloc or fnmatch.fnmatch(name=parsed_url.netloc, pat=pattern):
            proxy = "_none_"
            break

    return proxy


def _clear_cache(search_root: Path):
    """
    Clear the cache for a given Path.
    """
    temp_paths = list(search_root.rglob("hoppr-tmp-*"))
    for folder in temp_paths:
        if os.path.isdir(folder):
            shutil.rmtree(folder, ignore_errors=True)
        else:
            folder.unlink()


class CollectDnfPlugin(BatchCollectorPlugin):
    """
    Collector plugin for DNF packages
    """

    required_commands: list[str] = ["dnf"]
    supported_purl_types: list[str] = ["rpm"]
    products: list[str] = ["rpm/*"]

    def __init__(
        self,
        context: HopprContext,
        config: dict | None = None,
        config_file: str | PathLike = Path.cwd() / ".hoppr-dnf" / "dnf.conf",
    ) -> None:
        super().__init__(context=context, config=config)

        self.password_list: list[str] = []
        self.manifest_repos: list[str] = [f"{repo.url}" for repo in self.context.repositories[PurlType.RPM]]
        self.config_file = Path(config_file)

        if self.config and "dnf_command" in self.config:
            self.required_commands = [self.config["dnf_command"]]

        self.base_command = [
            self.required_commands[0],
            "--quiet",
            "--disableexcludes=all",
            f"--config={self.config_file}",
            "--disablerepo=*",
            "--enablerepo=hoppr-tmp-*",
        ]

        self.debug_args = ["--verbose"]

    def _get_component_download_url(self, purl: PackageURL) -> str:
        artifact = _artifact_string(purl)

        command = [*self.base_command, "repoquery", "--location", artifact]
        run_result = self.run_command(command, self.password_list)

        # If RPM URL not found, no need to try downloading it
        if run_result.returncode != 0 or len(run_result.stdout.decode("utf-8")) == 0:
            msg = f"{self.required_commands[0]} failed to locate package for {purl}"
            self.get_logger().debug(msg=msg, indent_level=2)

            raise HopprPluginError(msg)

        # Taking the first URL if multiple are returned
        return run_result.stdout.decode("utf-8").strip().split("\n")[0]

    def _get_found_repo(self, found_url: str) -> str | None:
        """
        Identify the repository associated with the specified URL
        """
        return next((repo for repo in self.manifest_repos if found_url.startswith(repo)), None)

    def get_version(self) -> str:
        return __version__

    @hoppr_process
    def pre_stage_process(self) -> Result:
        repo_config = ConfigParser()
        repo_config["main"] = {"cachedir": f"{self.config_file.parent / 'cache'}"}

        # Clear out cache before starting the pre_stage_process
        search_root = self.config_file.parent / "cache"
        _clear_cache(search_root)

        for idx, repo in enumerate(self.context.repositories[PurlType.RPM]):
            temp_repo = f"hoppr-tmp-{idx}"
            creds = Credentials.find(f"{repo.url}")
            if not _is_rpm_repo(f"{repo.url}"):
                self.get_logger().warning(
                    "Repo %s is not an RPM repository (repomd.xml file not found), will not be searched", repo.url
                )
                continue

            self.get_logger().debug("Creating repo %s for url %s", temp_repo, repo.url)

            # Create temporary repository file
            repo_config[temp_repo] = {
                "baseurl": f"{repo.url}",
                "enabled": "1",
                "name": f"Hoppr temp repository {idx}",
                "priority": "1",
                "proxy": _repo_proxy(f"{repo.url}"),
                "module_hotfixes": "true",
            }

            if creds is not None and isinstance(creds.password, SecretStr):
                repo_config[temp_repo]["username"] = f"{creds.username}"
                repo_config[temp_repo]["password"] = f"{creds.password.get_secret_value()}"

        if not self.context.strict_repos:
            system_repos = ConfigParser()

            # Get all system-managed .repo files
            repo_files = Path("/", "etc", "yum.repos.d").glob("*.repo")
            system_repos.read([str(repo_file) for repo_file in repo_files])

            # Get enabled system repos and add to temporary repository file
            for section in system_repos.sections():
                if system_repos[section]["enabled"] == "1":
                    repo_config.add_section(section)
                    repo_config[section] = dict(system_repos[section])

        try:
            # Create repo config dir in user directory
            config_dir = self.config_file.parent
            config_dir.mkdir(parents=True, exist_ok=True)
            with self.config_file.open(mode="w+", encoding="utf-8") as repo_file:
                repo_config.write(repo_file, space_around_delimiters=False)
        except OSError as ex:
            return Result.fail(f"Unable to write DNF repository config file: {ex}")

        # Populate user DNF cache
        command = [
            *self.base_command,
            "check-update",
            "makecache",
            *(self.debug_args if self.get_logger().is_verbose() else []),
        ]

        # Generate cache to use when downloading components
        result = self.run_command(command, self.password_list)
        self.get_logger().debug(msg=(f"Return Code: {result.returncode}"), indent_level=2)
        if result.returncode != 0:
            if hoppr.utils.get_partition(config_dir).fstype == "vboxsf":
                self.get_logger().warning(
                    "NOTE: Possible attempt to run DNF from a shared vagrant directory('%s'). "
                    "Recommend retrying outside of the shared vagrant directory",
                    config_dir,
                )
            return Result.fail(message="Failed to populate DNF cache.")

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure
        """

        purl = hoppr.utils.get_package_url(comp.purl)

        self.get_logger().info(msg=f"Copying DNF package from {purl}", indent_level=2)

        # Try getting RPM URL
        try:
            found_url = self._get_component_download_url(purl)
        except HopprPluginError as ex:
            return Result.retry(message=str(ex))

        repo = self._get_found_repo(found_url)
        # Return failure if found RPM URL is not from a repo defined in the manifest
        if repo is None:
            return Result.fail(
                "Successfully found RPM file but URL does not match any repository in manifest."
                f" (Found URL: '{found_url}')"
            )

        result = self.check_purl_specified_url(purl, repo)
        if not result.is_success():
            return result

        found_url_path = Path(found_url)
        subdir = found_url_path.relative_to(repo).parent
        target_dir = self.directory_for(purl.type, repo, subdir=str(subdir))

        # Download the RPM file to the new directory
        response = hoppr.net.download_file(
            url=found_url, dest=str(target_dir / found_url_path.name), creds=Credentials.find(url=repo)
        )
        result = Result.from_http_response(response)

        if result.is_retry():
            msg = f"Failed to download DNF artifact {purl.name} version {purl.version} from {found_url}"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.retry(message=msg)

        if result.is_success():
            self.set_collection_params(comp, repo, target_dir)
            result = Result.success(result.message, return_obj=comp)

        return result

    @hoppr_process
    def post_stage_process(self) -> Result:
        # Find repodata folders created when cache was generated
        search_root = self.config_file.parent / "cache"
        paths = list(search_root.rglob("hoppr-tmp-*/repodata"))

        repo_config = ConfigParser()
        repo_config.read(filenames=self.config_file, encoding="utf-8")

        msg = "Copying DNF repodata into bundle"
        self.get_logger().info(msg)
        self.notify(msg, type(self).__name__)

        # Loop over repos defined in the temp dnf.conf file
        for section in repo_config.sections():
            # Loop over repodata folders in DNF cache
            for folder in paths:
                # Check if full repodata path contains temp repo name
                if section in str(folder):
                    # Get temp repo's URL as defined in manifest
                    repo_url = repo_config[section]["baseurl"]
                    target_dir = self.context.collect_root_dir / "rpm" / quote_plus(repo_url) / "repodata"

                    shutil.copytree(src=folder, dst=target_dir, dirs_exist_ok=True)

        msg = f"Removing config file {self.config_file}"
        self.get_logger().info(msg)
        self.notify(msg, type(self).__name__)

        if self.config_file.exists():
            try:
                self.config_file.unlink()
            except FileNotFoundError as ex:
                return Result.fail(f"Failed to remove temporary DNF config file: {ex}")

        msg = "Removing cached DNF repodata"
        self.get_logger().info(msg)
        self.notify(msg, type(self).__name__)

        # Clear cache at the end of the post stage process
        _clear_cache(search_root)

        return Result.success()
