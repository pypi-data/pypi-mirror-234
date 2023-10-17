"""
Collector plugin to copy artifacts using the Nexus API
"""
from __future__ import annotations

import json
import re
import time

from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

import requests

from pydantic import SecretStr
from requests.auth import HTTPBasicAuth

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.types import PurlType, RepositoryUrl
from hoppr.net import download_file
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL


class CollectNexusSearch(SerialCollectorPlugin):
    """
    Class to copy artifacts using the Nexus API
    """

    # Unless specified by the user, all types except `git`, `github`, and `gitlab` are supported
    supported_purl_types: list[str] = [value for value in PurlType.values() if value not in {"git", "github", "gitlab"}]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.supported_purl_types = (self.config or {}).get("purl_types", type(self).supported_purl_types)

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """
        Collect artifact from Nexus
        """

        auth: HTTPBasicAuth | None = None
        if creds is not None and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

        nexus_url = self._parse_nexus_url(repo_url)[0]

        if not CollectNexusSearch.is_nexus_instance(nexus_url, auth):
            return Result.fail(f"{nexus_url} is not a Nexus instance")

        purl = hoppr.utils.get_package_url(comp.purl)

        source_urls = CollectNexusSearch.get_download_urls(purl, repo_url, auth)
        if len(source_urls) == 0:
            msg = f"No artifacts found in Nexus instance {repo_url} for purl {comp.purl}"
            self.get_logger().error(msg, indent_level=2)
            return Result.fail(msg)

        target_dir = self._directory_for_nexus(purl, source_urls[0])

        for source_url in source_urls:
            self.get_logger().info(
                msg=f"Collecting from {source_url}",
                indent_level=2,
            )

            file_name = Path(urlparse(source_url).path).parts[-1]

            response = download_file(source_url, str(target_dir / file_name))
            nexus_result = Result.from_http_response(response)

            self.get_logger().info("Download Result: %s", nexus_result, indent_level=3)

            if not nexus_result.is_success():
                return nexus_result

        self.set_collection_params(comp, repo_url, target_dir)
        return Result.success(return_obj=comp)

    @staticmethod
    def _parse_nexus_url(repo_url: str) -> tuple[str, str | None]:
        nexus_url = repo_url
        nexus_repo = None
        if repo_specified := re.search(r"(https?://.*?)/repository/(.*?)(/.*)?$", nexus_url):
            nexus_url = repo_specified[1]
            nexus_repo = repo_specified[2]

        return (nexus_url, nexus_repo)

    def _directory_for_nexus(self, purl: PackageURL, url: str) -> Path:
        if repo_match := re.search(r"(.*?/repository/.*?)(/.*)?/(.*)", url):
            nexus_repo = repo_match[1]
            path = repo_match[2]
            if path is not None:
                path = path[1:]

        subdir = None
        match purl.type:
            case "docker" | "generic" | "maven" | "raw" | "rpm":
                subdir = path
            case "helm" | "pypi":
                subdir = f"{purl.name}_{purl.version}"

        return self.directory_for(purl.type, nexus_repo, subdir=subdir)

    @staticmethod
    def is_nexus_instance(repo_url: str, auth: HTTPBasicAuth | None = None) -> bool:
        """
        Checks whether or not the repo_url refers to a Nexus instance
        """
        test_url = RepositoryUrl(url=repo_url) / "service" / "rest" / "v1" / "status"

        for attempt in range(3):
            if attempt > 0:
                time.sleep(5)

            response = requests.get(
                f"{test_url}",
                auth=auth,
                allow_redirects=True,
                stream=True,
                verify=True,
                timeout=60,
            )

            if response.status_code < 300:
                return True
            if response.status_code < 500:
                return False

        return False

    @staticmethod
    def get_download_urls(purl: PackageURL, repo_url: str, auth: HTTPBasicAuth | None = None) -> list[str]:
        """
        Retrieves all urls to be retrieved from Nexus for this component
        """
        nexus_url, nexus_repo = CollectNexusSearch._parse_nexus_url(repo_url)
        search_url = RepositoryUrl(url=nexus_url) / "service" / "rest" / "v1" / "search" / "assets"

        additional_search_params: list[dict] = [{}]
        nexus_format = purl.type
        match purl.type:
            case "deb":
                nexus_format = "apt"
            case "gem":
                nexus_format = "rubygems"
            case "golang":
                nexus_format = "go"
            case "generic" | "raw":
                nexus_format = "raw"
            case "maven":
                nexus_format = "maven2"
                additional_search_params = [
                    {"maven.extension": "jar", "maven.classifier": ""},
                    {"maven.extension": "jar", "maven.classifier": "sources"},
                    {"maven.extension": "pom"},
                ]
            case "rpm" | "yum":
                nexus_format = "yum"
                arch = purl.qualifiers.get("arch")
                additional_search_params = [{"yum.architecture": arch}] if arch is not None else [{}]

        base_params = {"sort": "version", "name": purl.name, "format": nexus_format}

        if purl.version is not None:
            base_params["version"] = purl.version

        if nexus_repo is not None:
            base_params["repository"] = nexus_repo

        url_list = []
        for extra_search_parms in additional_search_params:
            response = requests.get(
                f"{search_url}",
                auth=auth,
                allow_redirects=True,
                stream=True,
                verify=True,
                timeout=60,
                params=base_params | extra_search_parms,
            )

            if response.status_code < 300:
                search_result = json.loads(response.content)
                for item in search_result["items"]:
                    if item["downloadUrl"].startswith(repo_url):
                        url_list.append(item["downloadUrl"])
                        break

        return url_list

    @classmethod
    def get_attestation_products(cls, config: dict | None = None) -> list[str]:
        products: list[str] = []

        if config is not None and "purl_types" in config:
            products.extend(f"{purl_type}/*" for purl_type in config["purl_types"])
        else:
            products.extend(
                f"{purl_type}/*" for purl_type in PurlType if str(purl_type) not in ["git", "github", "gitlab"]
            )

        return products
