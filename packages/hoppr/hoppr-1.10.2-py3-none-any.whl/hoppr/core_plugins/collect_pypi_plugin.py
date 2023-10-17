"""
Collector plugin for pypi images
"""
from __future__ import annotations

import importlib.util
import re
import sys

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


class CollectPypiPlugin(SerialCollectorPlugin):
    """
    Collector plugin for pypi images
    """

    supported_purl_types = ["pypi"]
    required_commands = [sys.executable]
    products: list[str] = ["pypi/*"]
    system_repositories = ["https://pypi.org/simple"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.manifest_repos: list[str] = []
        self.password_list: list[str] = []
        self.base_command = [self.required_commands[0], "-m", "pip"]

        # Allow users to define their own pip command (e.g. "python3.6 -m pip")
        self.base_command = (self.config or {}).get("pip_command", f"{self.required_commands[0]} -m pip").split(" ")

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """
        Copy a component to the local collection directory structure
        """
        if importlib.util.find_spec(name="pip") is None:
            return Result.fail(message="The pip package was not found. Please install and try again.")

        purl = hoppr.utils.get_package_url(comp.purl)

        source_url = RepositoryUrl(url=repo_url)
        if not re.match(pattern="^.*simple/?$", string=f"{source_url}"):
            source_url /= "simple"

        password_list = []

        if creds is not None and isinstance(creds.password, SecretStr):
            source_url = RepositoryUrl(
                url=source_url.url,
                username=creds.username,
                password=creds.password.get_secret_value(),
            )
            password_list = [creds.password.get_secret_value()]

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")

        self.get_logger().info(msg=f"Target directory: {target_dir}", indent_level=2)

        command = [
            *self.base_command,
            "download",
            "--no-deps",
            "--no-cache",
            "--timeout",
            str(self.process_timeout),
            "--index-url",
            f"{source_url}",
            "--dest",
            f"{target_dir}",
            f"{purl.name}=={purl.version}",
            *(["--verbose"] if self.get_logger().is_verbose() else []),
        ]

        base_error_msg = f"Failed to download {purl.name} version {purl.version}"

        collection_type = "binary-preferred"
        if self.config is not None and "type" in self.config:
            collection_type = str(self.config["type"]).lower()

        success_count = 0
        successes_needed = 2 if collection_type == "both-required" else 1
        match collection_type:
            case "binary" | "binary-only" | "binary-preferred" | "both-preferred" | "both-required":
                type_order = ["binary", "source"]
            case "source" | "source-only" | "source-preferred":
                type_order = ["source", "binary"]
            case _:
                return Result.fail(
                    f"{base_error_msg}. Invalid pypi collection type specified: {collection_type}", return_obj=comp
                )

        self.get_logger().info("Pypi collection type: %s", collection_type, indent_level=2)
        self.get_logger().info("Attempting %s collection", type_order[0], indent_level=2)

        run_result = self.run_command([*command, self._pypi_param_for_type(type_order[0])], password_list)

        if run_result.returncode == 0:
            success_count += 1

            if not collection_type.startswith("both"):
                self.get_logger().debug(
                    "Collection of %s successful, no %s collection needed", type_order[0], type_order[1], indent_level=2
                )
                self.set_collection_params(comp, repo_url, target_dir)

                return Result.success(return_obj=comp)
        elif not collection_type.endswith("preferred"):
            self.get_logger().debug(
                "Collection of %s failed, no %s collection needed", type_order[0], type_order[1], indent_level=2
            )

            return Result.retry(f"{base_error_msg}. Unable to collect {type_order[0]}", comp)

        self.get_logger().info("Attempting %s collection", type_order[1], indent_level=2)

        run_result = self.run_command([*command, self._pypi_param_for_type(type_order[1])], password_list)

        if run_result.returncode == 0:
            success_count += 1

        if success_count >= successes_needed:
            self.set_collection_params(comp, repo_url, target_dir)
            return self._success_result(collection_type, type_order, success_count, run_result.returncode, comp)

        return self._retry_result(collection_type, type_order, success_count, base_error_msg, comp)

    @staticmethod
    def _success_result(
        collection_type: str, type_order: list[str], success_count: int, last_rc: int, comp: Component
    ) -> Result:
        message = ""
        match collection_type:
            case "binary-preferred" | "source-preferred":
                message = f"Unable to download {type_order[0]}, {type_order[1]} collected"
            case "both-preferred" if success_count == 1 and last_rc == 0:
                message = f"Only able to download {type_order[1]}"
            case "both-preferred" if success_count == 1:
                message = f"Only able to download {type_order[0]}"

        return Result.success(message, return_obj=comp)

    @staticmethod
    def _retry_result(
        collection_type: str, type_order: list[str], success_count: int, base_error_msg: str, comp: Component
    ) -> Result:
        message = ""
        match collection_type:
            case "both-required" if success_count == 1:
                message = f"{base_error_msg}. Only able to download {type_order[0]}"
            case "binary-preferred" | "source-preferred" | "both-required" | "both-preferred":
                message = f"{base_error_msg}. Unable to download {type_order[0]} or {type_order[1]}."

        return Result.retry(message, return_obj=comp)

    @staticmethod
    def _pypi_param_for_type(collection_type: str) -> str:
        if collection_type == "source":
            return "--no-binary=:all:"

        return "--only-binary=:all:"
