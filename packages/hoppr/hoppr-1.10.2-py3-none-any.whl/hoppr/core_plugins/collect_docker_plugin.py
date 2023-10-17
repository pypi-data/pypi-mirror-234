"""
Collector plugin for docker images
"""
from __future__ import annotations

import re
import urllib.parse

from pathlib import Path
from subprocess import CalledProcessError

from packageurl import PackageURL

from pydantic import SecretStr

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result


class CollectDockerPlugin(SerialCollectorPlugin):
    """
    Collector plugin for docker images
    """

    supported_purl_types = ["docker", "oci"]
    required_commands = ["skopeo"]
    products: list[str] = ["docker/*", "oci/*"]
    system_repositories: list[str] = ["https://docker.io/"]
    process_timeout = 300

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)
        self.required_commands = (self.config or {}).get("skopeo_command", self.required_commands)

    def _get_image(self, url: str, purl: PackageURL) -> RepositoryUrl:
        """
        Return the image details for skopeo to process

        Args:
            url (str): Repository URL
            purl (PackageURL): Purl of component to operate on

        Returns:
            RepositoryUrl: Image information
        """
        # Determine if purl version contains SHA string, determine proper formatting for skopeo command
        match purl.version:
            case no_sha if re.search(r"^(sha256:)?[a-fA-F0-9]{12,64}$", no_sha) is None:
                image_name = f"{purl.name}:{purl.version}"
            case sha if sha.startswith("sha256:"):
                image_name = f"{purl.name}@{purl.version}"
            case _:
                image_name = f"{purl.name}@sha256:{purl.version}"

        if purl.type == "oci" and "repository_url" in purl.qualifiers:
            url = purl.qualifiers.get("repository_url", "")
            url = url.replace(purl.name, "")

        source_image = RepositoryUrl(url=url) / (purl.namespace or "") / urllib.parse.quote_plus(image_name)

        if source_image.scheme != "docker":
            source_image = RepositoryUrl(url="docker://" + re.sub(r"^(.*://)", "", str(source_image)))

        return source_image

    def _get_target_path(self, repo_url: str, purl: PackageURL) -> Path:
        """
        Get target path for image download

        Args:
            repo_url (str): Repository URL
            purl (PackageURL): Purl of component to operate on

        Returns:
            Path: Filesystem location for downloaded image
        """
        version = re.sub(pattern=r"^(sha256:)?([a-f0-9]{64})$", repl=r"sha256:\2", string=purl.version)

        version = urllib.parse.quote_plus(re.sub(r"^https?://", "", version))
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

        return target_dir / f"{purl.name}@{version}"

    def _inspect_image(self, source_image: RepositoryUrl, purl: PackageURL) -> Result:
        """
        Verify provided image tag digest matches PURL version

        Args:
            source_image (RepositoryUrl): Full image name
            purl (PackageURL): Purl of component to operate on

        Returns:
            Result: The result of the verification
        """
        image_prefix, _ = source_image.url.rsplit("/", maxsplit=1)
        image_id = f"{purl.name}:{purl.qualifiers.get('tag')}"

        command = [self.required_commands[0], "inspect", "--format", "{{.Digest}}", f"{image_prefix}/{image_id}"]
        inspect_command = self.run_command(command)

        try:
            inspect_command.check_returncode()
            sha_tag = inspect_command.stdout.decode().strip()
        except CalledProcessError:
            return Result.retry(message=f"Failed to get image digest for '{source_image}'")

        if sha_tag != purl.version:
            return Result.fail(
                message=f"Provided tag '{purl.qualifiers.get('tag')}' image digest does not match '{purl.version}'"
            )

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None):
        """
        Copy a component to the local collection directory structure
        """
        purl = hoppr.utils.get_package_url(comp.purl)
        source_image = self._get_image(url=repo_url, purl=purl)
        target_path = self._get_target_path(repo_url, purl)

        if purl.type == "oci" and "tag" in purl.qualifiers:
            if not (inspect_result := self._inspect_image(source_image, purl)).is_success():
                return inspect_result

        self.get_logger().info(msg=f"Copying {purl.type} image:", indent_level=2)
        self.get_logger().info(msg=f"source: {source_image}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_path}", indent_level=3)

        command = [self.required_commands[0], "copy"]
        password_list = []

        if creds is not None and isinstance(creds.password, SecretStr):
            password_list = [creds.password.get_secret_value()]
            command = [*command, "--src-creds", f"{creds.username}:{creds.password.get_secret_value()}"]

        if re.match("^http://", repo_url):
            command = [*command, "--src-tls-verify=false"]

        if self.get_logger().is_verbose():
            command = [*command, "--debug"]

        command = [*command, urllib.parse.unquote(str(source_image)), f"{purl.type}-archive:{target_path}"]
        copy_result = self.run_command(command, password_list)

        try:
            copy_result.check_returncode()
        except CalledProcessError as ex:
            msg = f"Skopeo failed to copy {purl.type} image to {target_path}, return_code={ex.returncode}"
            self.get_logger().debug(msg=msg, indent_level=2)

            self.get_logger().info(msg="Artifact collection failed, deleting file and retrying", indent_level=2)
            target_path.unlink(missing_ok=True)

            return Result.retry(message=msg)

        self.set_collection_params(comp, repo_url, target_path.parent)

        return Result.success(return_obj=comp)
