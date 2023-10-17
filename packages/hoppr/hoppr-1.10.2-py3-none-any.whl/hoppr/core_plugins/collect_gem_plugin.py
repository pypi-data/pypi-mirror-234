"""
Collector plugin for Gem packages
"""
from __future__ import annotations

import jmespath
import requests

from requests import HTTPError

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result


class CollectGemPlugin(SerialCollectorPlugin):
    """
    Collector plugin for Gem packages
    """

    supported_purl_types = ["gem"]
    products: list[str] = ["gem/*"]
    system_repositories: list[str] = ["https://rubygems.org/api/v2/rubygems"]

    def get_version(self):
        return __version__

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)

        api_url = RepositoryUrl(url=repo_url) / purl.name / "versions" / f"{purl.version}.json"

        if platform := purl.qualifiers.get("platform"):
            api_url = RepositoryUrl(url=f"{api_url}?platform={platform}")

        response = requests.get(str(api_url), timeout=60)

        try:
            response.raise_for_status()
        except HTTPError:
            msg = f"RubyGems API web request error, request URL='{api_url}', status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        download_url: str | None = jmespath.search(expression="gem_uri", data=response.json())

        if not download_url:
            msg = f"Unable to retrieve download URL for Gem '{comp.purl}'"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        self.get_logger().info(msg=f"Copying Gem package from {api_url}", indent_level=2)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        self.get_logger().info(msg=target_dir.as_posix())

        package_out_path = target_dir / f"{purl.name}-{purl.version}.gem"

        self.get_logger().info(msg="Downloading Gem:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {package_out_path}", indent_level=3)

        response = hoppr.net.download_file(url=download_url, dest=str(package_out_path))

        result = Result.from_http_response(response=response, return_obj=comp)

        if not result.is_success():
            msg = f"Failed to download Gem package {comp.purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        self.set_collection_params(comp, repo_url, target_dir)
        return Result.success(return_obj=comp)
