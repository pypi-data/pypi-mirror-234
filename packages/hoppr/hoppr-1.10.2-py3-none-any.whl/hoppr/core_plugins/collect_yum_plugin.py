"""
Collector plugin for Yum packages
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models import HopprContext
from hoppr.result import Result


def _artifact_string(purl):
    artifact_string = purl.name
    if purl.version is not None:
        artifact_string += f"-{purl.version}"

    # Limiting to an architecture using --archlist finds all compatible architectures,
    # not just the specified one, so . . .
    if "arch" in purl.qualifiers:
        artifact_string += f"*{purl.qualifiers.get('arch')}"

    return artifact_string


class CollectYumPlugin(SerialCollectorPlugin):
    """
    Collector plugin for yum images
    """

    supported_purl_types = ["rpm"]
    required_commands = ["yumdownloader"]
    products: list[str] = ["rpm/*"]

    def get_version(self) -> str:
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)
        self.required_commands = (self.config or {}).get("yumdownloader_command", self.required_commands)

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds=None):
        """
        Copy a component to the local collection directory structure
        """

        purl = hoppr.utils.get_package_url(comp.purl)
        artifact = _artifact_string(purl)

        self.get_logger().info(msg=f"Copying yum package from {comp.purl}", indent_level=2)

        command = [
            self.required_commands[0],
            "-q",
            "--disableexcludes=all",
            "--setopt=*.module_hotfixes=true",
            "--downloadonly",
            "--urls",
            artifact,
        ]

        if self.get_logger().is_verbose():
            command = [*command, "--verbose"]

        run_result = self.run_command(command)
        if run_result.returncode != 0:
            msg = (
                f"{self.required_commands[0]} failed to locate package for {comp.purl}, "
                f"return_code={run_result.returncode}"
            )
            self.get_logger().debug(msg=msg, indent_level=2)

            return Result.retry(message=msg)

        # Taking the first URL if multiple are returned
        found_url = run_result.stdout.decode("utf-8").strip().split("\n")[0]

        if not found_url.startswith(repo_url):
            msg = "Yum download url does not match requested url."

            self.get_logger().error(msg=msg, indent_level=2)
            self.get_logger().error(msg=f"Yum download url:      {found_url}", indent_level=3)
            self.get_logger().error(msg=f"Expected url starting: {repo_url}", indent_level=3)

            return Result.fail(message=msg)

        found_url_path = Path(found_url)
        subdir = "/".join(found_url_path.parts[len(Path(repo_url).parts) : -1])
        target_dir = self.directory_for(purl.type, repo_url, subdir=subdir)

        command = [
            self.required_commands[0],
            "-q",
            "--disableexcludes=all",
            "--setopt=*.module_hotfixes=true",
            "--downloadonly",
            f"--destdir={target_dir}",
            artifact,
        ]

        run_result = self.run_command(command, [])
        if run_result.returncode != 0:
            msg = f"Failed to download Yum artifact {purl.name} version {purl.version} "
            return Result.retry(message=msg)

        self.set_collection_params(comp, repo_url, target_dir)

        return Result.success(return_obj=comp)
