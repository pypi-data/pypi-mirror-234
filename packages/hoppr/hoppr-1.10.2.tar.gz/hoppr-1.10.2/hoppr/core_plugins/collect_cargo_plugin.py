"""
Collector plugin for Cargo packages
"""
from __future__ import annotations
from pydantic import SecretStr

import requests

from requests import HTTPError
from requests.auth import HTTPBasicAuth

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result


class CollectCargoPlugin(SerialCollectorPlugin):
    """
    Collector plugin for Cargo packages
    """

    supported_purl_types = ["cargo"]
    products: list[str] = ["cargo/*"]
    system_repositories: list[str] = ["https://crates.io/api/v1/crates"]

    def get_version(self):
        return __version__

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        # pylint: disable=duplicate-code
        purl = hoppr.utils.get_package_url(comp.purl)
        cargo_url = RepositoryUrl(url=repo_url) / purl.name / (purl.version or "") / "download"

        self.get_logger().info(msg=f"Copying Cargo package from {cargo_url}", indent_level=2)

        authentication = None
        if creds is not None and isinstance(creds.password, SecretStr):
            authentication = HTTPBasicAuth(creds.username, creds.password.get_secret_value())

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / f"{purl.name}-{purl.version}.crate"

        response = requests.get(
            str(cargo_url),
            auth=authentication,
            timeout=300,
            proxies=self._get_proxies_for(repo_url),
            stream=True,
        )

        try:
            response.raise_for_status()
        except HTTPError:
            msg = f"Failed to download Cargo package {comp.purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        with package_out_path.open(mode="ab") as out_file:
            for chunk in response.iter_content(chunk_size=None):
                out_file.write(chunk)

        self.set_collection_params(comp, repo_url, target_dir)
        return Result.success(return_obj=comp)
