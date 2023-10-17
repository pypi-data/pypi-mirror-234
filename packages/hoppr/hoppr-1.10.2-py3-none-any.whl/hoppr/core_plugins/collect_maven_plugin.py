"""
Collector plugin for maven artifacts
"""
from __future__ import annotations

import os
import warnings

from copy import deepcopy
from pathlib import Path
from subprocess import CalledProcessError
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Any, OrderedDict

import jmespath
import xmltodict

from pydantic import SecretStr

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprExperimentalWarning
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL

_MAVEN_DEP_PLUGIN = "org.apache.maven.plugins:maven-dependency-plugin:3.5.0"


class _CollectMavenBase(SerialCollectorPlugin):
    supported_purl_types = ["maven"]
    required_commands = []
    products: list[str] = ["maven/*"]
    system_repositories: list[str] = ["https://repo.maven.apache.org/maven2"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.extra_opts: list[str] = []

        if self.config is not None:
            self.required_commands = self.config.get("maven_command", self.required_commands)
            self.extra_opts = self.config.get("maven_opts", self.extra_opts)

        system_settings_file = Path("/") / "etc" / "maven" / "settings.xml"
        user_settings_file = Path.home() / ".m2" / "settings.xml"

        if not self.context.strict_repos:
            # Identify system repositories
            for settings_file in [system_settings_file, user_settings_file]:
                if settings_file.is_file():
                    settings_dict: OrderedDict[str, Any] = xmltodict.parse(
                        settings_file.read_text(encoding="utf-8"),
                        encoding="utf-8",
                        force_list={"profile", "repository"},
                    )

                    repo_urls: list[str] = jmespath.search(
                        expression="settings.profiles.profile[].repositories.repository[].url", data=settings_dict
                    )

                    for repo in repo_urls or []:
                        if repo not in self.system_repositories:
                            self.system_repositories.append(repo)


if os.getenv("HOPPR_EXPERIMENTAL"):
    warnings.warn(
        message="This Maven collector plugin is experimental; use at your own risk.",
        category=HopprExperimentalWarning,
    )

    class CollectMavenPlugin(_CollectMavenBase):
        """
        Collector plugin for maven artifacts (EXPERIMENTAL)
        """

        def _check_artifact_hash(
            self,
            download_url: str,
            dest_file: str,
            creds: CredentialRequiredService | None = None,
        ) -> Result:
            with NamedTemporaryFile(mode="w+", encoding="utf-8") as hash_file:
                # Download SHA1 hash file for artifact
                response = hoppr.net.download_file(
                    url=f"{download_url}.sha1",
                    dest=hash_file.name,
                    creds=creds,
                    proxies=self._get_proxies_for(download_url),
                )

                result = Result.from_http_response(response=response)
                hash_string = Path(hash_file.name).read_text(encoding="utf-8")

            if not hoppr.net.check_hash(artifact=dest_file, hash_string=hash_string):
                result.merge(Result.fail(message=f"SHA1 hash for {Path(dest_file).name} does not match expected hash."))
                self.get_logger().debug(msg=f"Expected hash: {hash_string}", indent_level=2)

            return result

        def _get_maven_component(
            self,
            purl: PackageURL,
            repo_url: str,
            target_dir: Path,
            creds: CredentialRequiredService | None = None,
        ) -> Result:
            artifact_path = "/".join((purl.namespace or "").split("."))
            artifact_type = purl.qualifiers.get("type", "jar")
            artifact_classifier = purl.qualifiers.get("classifier")
            artifact_file = "-".join(
                filter(None, [purl.name, purl.version, "" if artifact_type == "pom" else artifact_classifier])
            )
            artifact_file = f"{artifact_file}.{artifact_type}"

            download_url = str(RepositoryUrl(url=repo_url) / artifact_path / purl.name / purl.version / artifact_file)
            dest_file = str(target_dir / artifact_file)

            self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
            self.get_logger().info(msg=f"destination: {dest_file}", indent_level=3)

            response = hoppr.net.download_file(
                url=download_url,
                dest=dest_file,
                creds=creds,
                proxies=self._get_proxies_for(download_url),
            )

            if not (result := Result.from_http_response(response=response)).is_success():
                return result

            result.merge(self._check_artifact_hash(download_url, dest_file, creds))

            return result

        @hoppr_rerunner
        def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
            purl = hoppr.utils.get_package_url(comp.purl)
            target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

            self.get_logger().info(msg="Downloading Maven artifact:", indent_level=2)
            result = self._get_maven_component(purl, repo_url, target_dir, creds)

            if not result.is_success():
                msg = f"Failed to download Maven artifact {comp.purl}, {result.message}"
                self.get_logger().error(msg=msg, indent_level=2)
                return Result.fail(message=msg)

            if purl.qualifiers.get("type") != "pom":
                self.get_logger().info(msg="Downloading pom for Maven artifact:", indent_level=2)

                purl_copy = deepcopy(purl)
                purl_copy.qualifiers["type"] = "pom"
                result = self._get_maven_component(purl_copy, repo_url, target_dir, creds)

                if not result.is_success():
                    msg = f"Failed to download pom for Maven artifact {comp.purl}, {result.message}"
                    self.get_logger().error(msg=msg, indent_level=2)
                    return Result.fail(message=msg)

            self.set_collection_params(comp, repo_url, target_dir)

            return Result.success(return_obj=comp)

else:

    class CollectMavenPlugin(_CollectMavenBase):  # type: ignore[no-redef]
        """
        Collector plugin for maven artifacts
        """

        required_commands = ["mvn"]

        def _get_maven_component(self, command: list[str], password_list: list[str], **kwargs):
            full_command = command.copy()
            full_command.extend(f"-D{key}={value}" for key, value in kwargs.items())
            result = self.run_command(full_command, password_list)

            # The maven plugin does not recognize the 'destFileName' argument, so rename the file
            if result.returncode == 0:
                _, name, version, extension = kwargs.get("artifact", "::::").split(":")
                directory = kwargs.get("outputDirectory", ".")
                old_name = f"{name}-{version}.{extension}"
                new_name = kwargs.get("destFileName", f"{name}-{version}.{extension}")

                os.rename(directory / old_name, directory / new_name)

            return result

        @hoppr_rerunner
        def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
            """
            Copy a component to the local collection directory structure
            """
            # pylint: disable=too-many-locals

            purl = hoppr.utils.get_package_url(comp.purl)
            artifact = f"{purl.namespace}:{purl.name}:{purl.version}"

            extension = purl.qualifiers.get("type", "tar.gz")
            target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

            self.get_logger().info(msg="Copying maven artifact:", indent_level=2)
            self.get_logger().info(msg=f"source: {repo_url}", indent_level=3)
            self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

            settings_dict = {
                "settings": {
                    "servers": {
                        "server": {
                            "id": "repoId",
                            "username": "${repo.login}",
                            "password": "${repo.pwd}",
                        }
                    }
                }
            }

            with NamedTemporaryFile(mode="w+", encoding="utf-8") as settings_file:
                settings_file.write(xmltodict.unparse(input_dict=settings_dict, pretty=True))
                settings_file.flush()

                password_list = []

                defines = {
                    "artifact": f"{artifact}:{extension}",
                    "outputDirectory": target_dir,
                    "destFileName": f"{purl.name}-{purl.version}.{extension}",
                    "remoteRepositories": f"repoId::::{repo_url}",
                }

                if creds is not None and isinstance(creds.password, SecretStr):
                    defines["repo.login"] = creds.username
                    defines["repo.pwd"] = creds.password.get_secret_value()
                    password_list = [creds.password.get_secret_value()]

                command = [
                    self.required_commands[0],
                    f"{_MAVEN_DEP_PLUGIN}:copy",
                    f"--settings={settings_file.name}",
                    *self.extra_opts,
                    *(["--debug"] if self.get_logger().is_verbose() else []),
                ]

                run_result = self._get_maven_component(command, password_list, **defines)
                error_msg = f"Failed to download maven artifact {artifact} type={extension}"

                try:
                    run_result.check_returncode()

                    if extension != "pom":
                        defines["artifact"] = str(defines["artifact"]).replace(f":{extension}", ":pom")
                        defines["destFileName"] = str(defines["destFileName"]).replace(f".{extension}", ".pom")

                        error_msg = f"Failed to download pom for maven artifact {artifact}"
                        run_result = self._get_maven_component(command, password_list, **defines)
                        run_result.check_returncode()
                except CalledProcessError:
                    self.get_logger().debug(msg=error_msg, indent_level=2)
                    return Result.retry(message=error_msg)

            self.set_collection_params(comp, repo_url, target_dir)

            return Result.success(return_obj=comp)
