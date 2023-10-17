"""
Collector plugin for npm packages
"""
from __future__ import annotations

from urllib.parse import quote_plus
from pydantic import SecretStr

import requests

from requests.auth import HTTPBasicAuth

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result


class CollectNpmPlugin(SerialCollectorPlugin):
    """
    Collector plugin for npm packages
    """

    supported_purl_types: list[str] = ["npm"]
    products: list[str] = ["npm/*"]
    system_repositories: list[str] = ["https://registry.npmjs.org"]

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

    def get_version(self):
        return __version__

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """
        Download npm package via get request
        """
        purl = hoppr.utils.get_package_url(comp.purl)
        self.get_logger().info(msg=f"Copying npm package from {comp.purl}", indent_level=2)

        tar_name = f"{purl.name}{f'-{purl.version}' if purl.version else ''}.tgz"
        npm_url = RepositoryUrl(url=repo_url) / quote_plus(purl.namespace or "") / purl.name / "-" / tar_name

        authentication = None
        if creds is not None and isinstance(creds.password, SecretStr):
            authentication = HTTPBasicAuth(creds.username, creds.password.get_secret_value())

        response = requests.get(npm_url.url, auth=authentication, timeout=300, proxies=self._get_proxies_for(repo_url))

        if response.status_code not in range(200, 300):
            msg = f"Failed to locate npm package for {comp.purl}, return_code={response.status_code}"
            self.get_logger().debug(msg=msg, indent_level=2)

            return Result.retry(message=msg)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / tar_name
        package_out_path.write_bytes(response.content)

        self.set_collection_params(comp, repo_url, target_dir)
        return Result.success(return_obj=comp)
