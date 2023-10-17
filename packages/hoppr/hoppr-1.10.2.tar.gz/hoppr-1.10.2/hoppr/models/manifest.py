"""
Manifest file data model
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, ClassVar, Literal, MutableMapping

from pydantic import Field, NoneStr, create_model, validator
from pydantic.main import ModelMetaclass
from requests import HTTPError
from typer import secho

import hoppr.net
import hoppr.oci_artifacts
import hoppr.utils

from hoppr.constants import BomProps
from hoppr.exceptions import HopprLoadDataError
from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel
from hoppr.models.sbom import Component, ExternalReference, Property, Sbom, SbomRef
from hoppr.models.types import LocalFile, OciFile, PurlType, RepositoryUrl, UrlFile

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny


class Repository(HopprBaseModel):
    """
    Repository data model
    """

    url: str = Field(
        ...,
        regex=r"^([^:/?#]+:(?=//))?(//)?(([^:]+(?::[^@]+?)?@)?[^@/?#:]*(?::\d+?)?)?[^?#]*(\?[^#]*)?(#.*)?",
    )
    description: NoneStr = None

    @validator("url", pre=True)
    @classmethod
    def validate_url_pre(cls, url: str | dict[str, str]) -> str:
        """
        Ensure URL is parsed as `str` before Pydantic validation
        """
        if isinstance(url, dict):
            url = url["url"]

        return str(url)

    @validator("url")
    @classmethod
    def validate_url(cls, url: str) -> RepositoryUrl:
        """
        Convert URL string to `RepositoryUrl` after validation
        """
        return RepositoryUrl(url=url)


# Dynamic Repositories model with PurlType values as attribute names
purl_type_repo_mapping = {str(purl_type): (list[Repository], Field([], unique_items=True)) for purl_type in PurlType}
RepositoriesMetaclass: ModelMetaclass = create_model(  # type: ignore[call-overload]
    "RepositoriesMetaclass", __base__=HopprBaseModel, **purl_type_repo_mapping
)


class Repositories(RepositoriesMetaclass):  # type: ignore[misc, valid-type]
    """
    Repositories data model
    """

    # pylint: disable=too-few-public-methods

    def __getitem__(self, item: str | PurlType) -> list[Repository]:
        return getattr(self, str(item), [])

    def __setitem__(self, item: str | PurlType, value: list[Repository]) -> None:
        setattr(self, str(item), value)

    def __iter__(self):
        for purl_type in PurlType:
            yield (purl_type, self[purl_type])


class SearchSequence(HopprBaseModel):
    """
    SearchSequence data model
    """

    version: Literal["v1"]
    repositories: list[RepositoryUrl | str] = []


IncludeRef = Annotated[LocalFile | UrlFile, Field(..., description="Reference to a local or remote manifest file")]
Includes = Annotated[list[IncludeRef], Field(..., description="List of manifest files to load")]
IncludeRefMap = Annotated[MutableMapping[IncludeRef, "ManifestFile"], Field(...)]


class ManifestFile(HopprBaseSchemaModel):
    """
    Data model to describe a single manifest file
    """

    kind: Literal["Manifest"]
    repositories: Repositories = Field(..., description="Maps supported PURL types to package repositories/registries")
    includes: Includes = []
    sboms: list[SbomRef] = []

    @classmethod
    def parse_file(cls, path: str | Path, *args, **kwargs) -> ManifestFile:  # pylint: disable=unused-argument
        """
        Override to resolve local file paths relative to manifest file
        """
        path = Path(path)

        data = hoppr.utils.load_file(path)
        if not isinstance(data, dict):
            raise TypeError("Local file content was not loaded as dictionary")

        # Resolve local file path references relative to manifest file path
        for sbom in data.get("sboms", []):
            if "local" in sbom:
                local_ref = (path.parent / sbom["local"]).resolve().relative_to(Path.cwd())
                sbom["local"] = str(local_ref)

        for include in data.get("includes", []):
            if "local" in include:
                local_ref = (path.parent / include["local"]).resolve().relative_to(Path.cwd())
                include["local"] = str(local_ref)

        return cls(**data)

    @classmethod
    def parse_obj(cls, obj: DictStrAny) -> ManifestFile:
        """
        Override to remove local file paths that can't be resolved
        """
        for include in list(obj.get("includes", [])):
            if "local" in include and not Path(include["local"]).is_absolute():
                secho(f"Skipping local include: relative path '{include['local']}' cannot be resolved", fg="yellow")
                obj["includes"].remove(include)

        for sbom in list(obj.get("sboms", [])):
            if "local" in sbom and not Path(sbom["local"]).is_absolute():
                secho(f"Skipping local SBOM: relative path '{sbom['local']}' cannot be resolved", fg="yellow")
                obj["sboms"].remove(sbom)

        return cls(**obj)


class Manifest(ManifestFile):
    """
    Manifest data model that generates lookups for `includes` and `sboms` references
    """

    consolidated_sbom: Annotated[Sbom, Field(exclude=True)] = None  # type: ignore[assignment]

    # Attributes not included in schema
    loaded_manifests: ClassVar[IncludeRefMap] = {}

    @validator("includes", allow_reuse=True, always=True)
    @classmethod
    def populate_loaded_manifests(cls, includes: Includes, values: DictStrAny) -> Includes:
        """
        Validator that automatically loads manifest from local file or URL into lookup dictionary
        """
        for include_ref in includes:
            if include_ref not in cls.loaded_manifests:
                match include_ref:
                    case LocalFile():
                        cls.loaded_manifests[include_ref] = ManifestFile.parse_file(include_ref.local)
                        loaded = cls.load(include_ref.local)
                    case UrlFile():
                        data = hoppr.net.load_url(include_ref.url)
                        if not isinstance(data, dict):
                            raise TypeError("URL manifest include was not loaded as dictionary")

                        cls.loaded_manifests[include_ref] = ManifestFile.parse_obj(data)
                        loaded = cls.load(include_ref.url)
                    case _:
                        continue

                # Add all repositories of current manifest to included manifest
                for purl_type in PurlType:
                    # List of repos for purl type in current manifest
                    combined_repos = deepcopy(values["repositories"][str(purl_type)])

                    # List of repos for purl type in included manifest
                    include_repos: list[Repository] = getattr(loaded.repositories, str(purl_type), [])

                    # Append each included manifest repo to list of current manifest repos
                    for repo in include_repos:
                        if repo not in combined_repos:
                            combined_repos.append(repo)

                    # Set included manifest repos to the combined list of repos for purl type
                    setattr(loaded.repositories, str(purl_type), combined_repos)

                cls.loaded_manifests[include_ref] = loaded

        return includes

    @validator("sboms", allow_reuse=True, always=True)
    @classmethod
    def populate_loaded_sboms(cls, sboms: list[SbomRef], values: DictStrAny) -> list[SbomRef]:
        """
        Validator that automatically loads SBOM from local file or URL into lookup dictionary
        """
        for sbom_ref in sboms:
            if sbom_ref not in Sbom.loaded_sboms:
                if (loaded_sbom := cls._load_sbom(sbom_ref)) is None:
                    continue

                # Merge current SBOM metadata into consolidated SBOM
                for component in loaded_sbom.components or []:
                    if not (purl_str := getattr(component, "purl", None)):
                        continue

                    purl_type = hoppr.utils.get_package_url(purl_str).type

                    # Generate the repository search sequence
                    search_sequence = SearchSequence(
                        version="v1", repositories=[str(repo.url) for repo in values["repositories"][purl_type]]
                    )

                    # Add repository search sequence as component property
                    component.properties.append(
                        Property(name=BomProps.COMPONENT_SEARCH_SEQUENCE, value=search_sequence.json())
                    )

                    # Add external reference to SBOM file that includes this component
                    component.externalReferences.append(
                        ExternalReference(
                            url=str(sbom_ref),
                            type="bom",  # type: ignore[arg-type]
                            comment=loaded_sbom.serialNumber,
                            hashes=None,
                        )
                    )

                    # Merge component into consolidated SBOM
                    cls._add_component(component)

        return sboms

    @validator("consolidated_sbom", allow_reuse=True, always=True)
    @classmethod
    def populate_consolidated_sbom(cls, consolidated_sbom: Sbom | None) -> Sbom:
        """
        Populate `consolidated_sbom` with previously loaded `components` and `externalReferences`
        """
        consolidated_sbom = Sbom()

        for sbom_ref, sbom in Sbom.loaded_sboms.items():
            external_ref = ExternalReference(
                url=str(sbom_ref),
                type="bom",  # type: ignore[arg-type]
                comment=sbom.serialNumber,
            )

            sbom.externalReferences = hoppr.utils.dedup_list([*sbom.externalReferences, external_ref])

            for component in sbom.components:
                component.externalReferences = hoppr.utils.dedup_list([*component.externalReferences, external_ref])

            consolidated_sbom.merge(sbom)

        return consolidated_sbom

    @classmethod
    def _add_component(cls, component: Component) -> None:
        # Merge component into previously loaded component
        if loaded := Component.find(component.bom_ref):
            loaded.merge(component)
        else:
            Component.unique_id_map[component.bom_ref] = component

    @classmethod
    def _load_sbom(cls, sbom_ref: SbomRef) -> Sbom | None:
        match sbom_ref:
            case LocalFile():
                return Sbom.load(sbom_ref.local)
            case OciFile():
                data = hoppr.oci_artifacts.pull_artifact(sbom_ref.oci)
                if not isinstance(data, dict):
                    raise TypeError("OCI URL SBOM file was not loaded as dictionary")

                return Sbom.load(data)
            case UrlFile():
                return Sbom.load(sbom_ref.url)
            case _:
                return None

    @classmethod
    def find(cls, ref_type: Literal["local", "url"], location: str | Path) -> ManifestFile | None:
        """
        Lookup manifest object by include reference

        Args:
            ref_type (Literal["local", "url"]): Type of include
            location (str | Path): Path to included manifest

        Returns:
            ManifestFile | None: Manifest object if found, otherwise None
        """
        match ref_type:
            case "local":
                location = Path(location).resolve().relative_to(Path.cwd())
                return cls.loaded_manifests.get(LocalFile(local=Path(location)))
            case "url":
                return cls.loaded_manifests.get(UrlFile(url=str(location)))
            case _:
                return None

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Manifest:
        """
        Load manifest from local file, URL, or dict
        """
        match source:
            case dict():
                data = source
            case Path():
                # Convert source to relative path if in current working directory subpath
                source = source.resolve()
                source = source.relative_to(Path.cwd()) if source.is_relative_to(Path.cwd()) else source

                manifest_file = cls.parse_file(source)
                cls.loaded_manifests[LocalFile(local=source)] = manifest_file
                data = manifest_file.dict(by_alias=True)
            case str():
                try:
                    include_dict = hoppr.net.load_url(source)
                    if not isinstance(include_dict, dict):
                        raise TypeError("URL manifest include was not loaded as dictionary")

                    manifest_file = cls.parse_obj(include_dict)
                    url_ref = UrlFile(url=source)
                    cls.loaded_manifests[url_ref] = manifest_file
                except (HopprLoadDataError, HTTPError) as ex:
                    raise HopprLoadDataError from ex

                data = manifest_file.dict(by_alias=True)

        return cls(**data)
