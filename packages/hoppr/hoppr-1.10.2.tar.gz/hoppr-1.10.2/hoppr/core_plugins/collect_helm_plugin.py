"""
Collector plugin for helm charts
"""
from __future__ import annotations

from pathlib import Path

from pydantic import SecretStr

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprLoadDataError
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result


class CollectHelmPlugin(SerialCollectorPlugin):
    """
    Class to copy helm charts
    """

    supported_purl_types = ["helm"]
    required_commands = ["helm"]
    products: list[str] = ["helm/*"]
    system_repositories: list[str] = []

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.required_commands = (self.config or {}).get("helm_command", self.required_commands)
        self.base_command = [self.required_commands[0], "fetch"]

        system_repos_file = Path.home() / ".config" / "helm" / "repositories.yaml"
        if not self.context.strict_repos and system_repos_file.exists():
            system_repos: list[dict[str, str]] = []

            try:
                system_repos_dict = hoppr.utils.load_file(input_file_path=system_repos_file)
                if not isinstance(system_repos_dict, dict):
                    raise HopprLoadDataError("Incorrect format.")

                system_repos = system_repos_dict["repositories"]
            except HopprLoadDataError as ex:
                self.get_logger().warning(msg=f"Unable to parse Helm repositories file ({system_repos_file}): '{ex}'")

            self.system_repositories.extend(repo["url"] for repo in system_repos)

    @hoppr_rerunner
    # pylint: disable=duplicate-code
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None):
        """
        Collect helm chart
        """

        purl = hoppr.utils.get_package_url(comp.purl)

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")

        run_result = None
        for subdir in ["", purl.name]:
            source_url = RepositoryUrl(url=repo_url) / subdir

            self.get_logger().info(msg="Fetching helm chart:", indent_level=2)
            self.get_logger().info(msg=f"source: {source_url}", indent_level=3)
            self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

            command = [
                *self.base_command,
                "--repo",
                f"{source_url}",
                "--destination",
                f"{target_dir}",
                purl.name,
                "--version",
                purl.version,
                *(["--debug"] if self.get_logger().is_verbose() else []),
            ]

            password_list = []

            if creds is not None and isinstance(creds.password, SecretStr):
                command = [
                    *command,
                    "--username",
                    creds.username,
                    "--password",
                    creds.password.get_secret_value(),
                ]

                password_list = [creds.password.get_secret_value()]

            run_result = self.run_command(command, password_list)

            if run_result.returncode == 0:
                self.get_logger().info("Complete helm chart artifact copy for %s version %s", purl.name, purl.version)
                self.set_collection_params(comp, repo_url, target_dir)

                return Result.success(return_obj=comp)

        msg = f"Failed to download {purl.name} version {purl.version} helm chart from {repo_url}."

        if run_result is not None and "404 Not Found" in str(run_result.stderr):
            self.get_logger().debug(msg=msg, indent_level=2)
            return Result.fail(f"{msg} Chart not found.")

        self.get_logger().debug(msg=msg, indent_level=2)
        return Result.retry(msg)
