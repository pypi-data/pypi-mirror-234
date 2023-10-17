"""
CycloneDX data models
"""
from __future__ import annotations

import uuid

from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Iterator, Literal, MutableMapping, TypeAlias, cast

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import Extra, Field, root_validator, validator
from rapidfuzz import fuzz
from requests import HTTPError

import hoppr.net
import hoppr.utils

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.affect import Affect
from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap
from hoppr.models.licenses import LicenseChoice
from hoppr.models.types import LocalFile, OciFile, UrlFile

if TYPE_CHECKING:
    from packageurl import PackageURL

DictStrAny: TypeAlias = dict[str, Any]

__all__ = [
    "Component",
    "ExternalReference",
    "Hash",
    "Property",
    "Sbom",
]

SbomRef = Annotated[LocalFile | OciFile | UrlFile, Field(..., description="Reference to a local or remote SBOM file")]
SbomRefMap = Annotated[MutableMapping[SbomRef, "Sbom"], Field(default=...)]

FUZZY_MATCH_THRESHOLD = 85


def _extract_components(components: list[Component]) -> list[Component]:
    """
    Explicitly set scope of flattened components to `exclude`
    """
    for component in components:
        setattr(component, "scope", "excluded")

    return hoppr.utils.dedup_list(components)


def _extract_sbom_components(external_refs: list[ExternalReference]) -> list[Component]:
    """
    Extracts `external_refs` of type "bom" and returns the set of their components
    """
    components: list[Component] = []

    for ref in _get_bom_refs(external_refs):
        sbom = Sbom.load(_resolve_sbom_source(ref.dict()["url"]))
        sbom.components = _extract_components(sbom.components)
        components.extend(sbom.components)
        external_refs.remove(ref)

    return components


def _flatten_component(component: Component) -> list[Component]:
    """
    Helper function to flatten a component's subcomponents into a set
    """
    flattened = []

    for subcomponent in component.components or []:
        # Ensure validator is run to set `bom_ref`
        subcomponent = Component(**subcomponent.dict())
        setattr(subcomponent, "scope", "excluded")

        # Flatten nested components into top level components list
        flattened.append(subcomponent)

    component.components.clear()
    return flattened


def _get_bom_refs(external_refs: list[ExternalReference]) -> Iterator[ExternalReference]:
    """
    Get `externalReferences` of type "bom"
    """
    yield from (ref.copy(deep=True) for ref in (external_refs or []) if ref.type == "bom")


def _resolve_sbom_source(source: str) -> str | Path | DictStrAny:
    """
    Resolves an SBOM source as a file path, URL or `dict`
    """
    return Path(source.removeprefix("file://")).resolve() if source.startswith("file://") else source


def _validate_components(cls, components: list[Component]) -> list[Component]:
    """
    Validator to optionally flatten `components` list
    """
    if not cls.flatten:
        return components

    flattened = list(components)

    for component in components:
        flattened.extend(_flatten_component(component))

    return hoppr.utils.dedup_list(flattened)


def _validate_external_refs(cls, external_refs: list[ExternalReference], values: DictStrAny) -> list[ExternalReference]:
    """
    Validator to optionally resolve `externalReferences`
    """
    external_refs = [ExternalReference.create(ref) for ref in external_refs or []]

    if cls.deep_merge:
        external_ref_components = _extract_sbom_components(external_refs)
        values["components"] = hoppr.utils.dedup_list([*values.get("components", []), *external_ref_components])

    return external_refs


class ExternalReference(CycloneDXBaseModel, cdx.ExternalReference):
    """
    ExternalReference data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for ExternalReference model"
        extra = Extra.allow

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Hash(CycloneDXBaseModel, cdx.Hash):
    """
    Hash data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Hash model"
        extra = Extra.allow

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Property(CycloneDXBaseModel, cdx.Property):
    """
    Property data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Property model"
        extra = Extra.allow

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Component(CycloneDXBaseModel, cdx.Component):
    """
    Component data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Component model"
        extra = Extra.allow

    bom_ref: Annotated[str, Field(alias="bom-ref")] = None  # type: ignore[assignment]
    components: list[Component] = []  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = []  # type: ignore[assignment]
    hashes: list[Hash] = []  # type: ignore[assignment]
    licenses: LicenseChoice = []  # type: ignore[assignment]
    properties: list[Property] = []  # type: ignore[assignment]

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components: classmethod = validator("components", allow_reuse=True, always=True)(_validate_components)
    validate_external_refs: classmethod = validator("externalReferences", allow_reuse=True)(_validate_external_refs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Component):
            return False

        if self.purl and other.purl:
            self_purl = hoppr.utils.get_package_url(self.purl)
            other_purl = hoppr.utils.get_package_url(other.purl)

            qual_keys = hoppr.utils.dedup_list({**self_purl.qualifiers, **other_purl.qualifiers})

            return all(
                [
                    self_purl.name == other_purl.name,
                    self_purl.type == other_purl.type,
                    self_purl.namespace == other_purl.namespace,
                    str(self_purl.version).removeprefix("v") == str(other_purl.version).removeprefix("v"),
                    self_purl.subpath == other_purl.subpath,
                    *[self._qualifier_match(key, self_purl, other_purl) for key in qual_keys],
                ]
            )

        if self.bom_ref and other.bom_ref:
            return self.bom_ref == other.bom_ref

        return False  # pragma: no cover

    @staticmethod
    def _qualifier_match(key: str, self_purl: PackageURL, other_purl: PackageURL) -> bool:
        # Compare only if both purls have a value for specified qualifier
        if key not in (self_qual := self_purl.qualifiers) or key not in (other_qual := other_purl.qualifiers):
            return True

        return fuzz.ratio(self_qual.get(key, ""), other_qual.get(key, "")) > FUZZY_MATCH_THRESHOLD

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_component(cls, values: DictStrAny) -> DictStrAny:
        """
        Validator to set a Component's `bom-ref` identifier if not set
        """
        if not any([values.get("purl"), values.get("bom-ref"), all([values.get("name"), values.get("version")])]):
            raise ValueError(
                "Either 'bom-ref' or 'purl' must be defined, or 'name' and 'version' must be defined on a component"
            )

        def _unescape_unicode(value: str) -> str:
            # Decode any unicode escape sequences, e.g. "\u0026" -> "&"
            return value.encode(encoding="utf-8").decode()

        if values.get("purl"):
            values["purl"] = _unescape_unicode(str(values["purl"]))

            if not values.get("version") and (version := hoppr.utils.get_package_url(values["purl"]).version):
                values["version"] = version

        bom_ref = str(
            values.get("purl")
            or f"{'@'.join(filter(None, [values.get('name'), values.get('version')]))}"
            or values.get("bom-ref")
        )

        values["bom-ref"] = _unescape_unicode(bom_ref)

        return values


Component.update_forward_refs()


class Vulnerability(CycloneDXBaseModel, cdx.Vulnerability):
    """
    Vulnerability data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Vulnerability model"
        extra = Extra.allow

    affects: Annotated[
        list[Affect],
        Field(description="The components or services that are affected by the vulnerability.", title="Affects"),
    ] = []  # type: ignore[assignment]

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Sbom(CycloneDXBaseModel, cdx.CyclonedxSoftwareBillOfMaterialsStandard):
    """
    Sbom data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Sbom model"

    components: list[Component] = []  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = []  # type: ignore[assignment]
    specVersion: str = "1.5"
    version: int = 1
    vulnerabilities: list[Vulnerability] = []  # type: ignore[assignment]

    # Attributes not included in schema
    loaded_sboms: ClassVar[SbomRefMap] = {}
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components: classmethod = validator("components", allow_reuse=True, always=True)(_validate_components)
    validate_external_refs: classmethod = validator("externalReferences", allow_reuse=True)(_validate_external_refs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sbom):
            return False

        return True if self.serialNumber == other.serialNumber else super().__eq__(other)

    @validator("metadata", allow_reuse=True, always=True)
    @classmethod
    def validate_metadata(cls, metadata: cdx.Metadata | None) -> cdx.Metadata:
        """
        Validator to populate and normalize `metadata` field
        """
        metadata = metadata or cdx.Metadata()

        # Generate `metadata` field containing Hoppr tool component
        hoppr_metadata: Any = CycloneDXBaseModel.create(cdx.Metadata(timestamp=datetime.now(timezone.utc)))
        hoppr_metadata.tools = CycloneDXBaseModel.create(cdx.ToolModel())
        hoppr_metadata.tools.components = [  # type: ignore[attr-defined]
            Component(
                type=cdx.Type("application"),
                name="hoppr",
                version=hoppr.__version__,
                bom_ref=f"pkg:pypi/hoppr@{hoppr.__version__}",
                purl=f"pkg:pypi/hoppr@{hoppr.__version__}",
                scope=cdx.Scope("excluded"),
            ),
        ]

        # Convert deprecated `list[Tool]` to `ToolModel` structure
        if isinstance(tools := metadata.tools, list):
            hoppr_metadata.tools.components.extend(  # type: ignore[attr-defined]
                hoppr.utils.dedup_list(
                    Component(
                        type=cdx.Type("application"),
                        name=str(tool.name),
                        version=tool.version,
                        hashes=[Hash.create(hash) for hash in tool.hashes or []],
                        externalReferences=[ExternalReference.create(ref) for ref in tool.externalReferences or []],
                        scope=cdx.Scope("excluded"),
                    )
                    for tool in tools
                )
            )

            metadata.tools = None

        # Merge any remaining metadata from the SBOM being validated into Hoppr metadata
        hoppr_metadata.merge(CycloneDXBaseModel.create(metadata or cdx.Metadata()))
        return cast(cdx.Metadata, hoppr_metadata)

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_sbom(cls, values: DictStrAny) -> DictStrAny:
        """
        Validator to standardize fields
        """
        values["$schema"] = "http://cyclonedx.org/schema/bom-1.5.schema.json"
        values["specVersion"] = "1.5"
        values["serialNumber"] = values.get("serialNumber", None) or uuid.uuid4().urn

        return values

    @classmethod
    def find_ref(cls, ref_type: Literal["local", "oci", "url"], location: str | Path) -> Sbom | None:
        """
        Look up SBOM object by reference

        Args:
            ref_type (Literal["local", "oci", "url"]): Type of SBOM reference
            location (str | Path): Location of SBOM reference

        Returns:
            Sbom | None: SBOM object if found, otherwise None
        """
        # pylint: disable=duplicate-code
        match ref_type:
            case "local":
                return cls.loaded_sboms.get(LocalFile(local=Path(location)), None)
            case "oci":
                return cls.loaded_sboms.get(OciFile(oci=str(location)), None)
            case "url":
                return cls.loaded_sboms.get(UrlFile(url=str(location)), None)
            case _:
                return None

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Sbom:
        """
        Load SBOM from local file, URL, or dict
        """
        # pylint: disable=duplicate-code
        match source:
            case dict():
                sbom = cls(**source)
            case Path():
                # Convert source to relative path if in current working directory subpath
                source = source.resolve()
                source = source.relative_to(Path.cwd()) if source.is_relative_to(Path.cwd()) else source

                sbom = cls.parse_file(source)
                cls.loaded_sboms[LocalFile(local=source)] = sbom
            case str():
                try:
                    sbom_dict = hoppr.net.load_url(source)
                    if not isinstance(sbom_dict, dict):
                        raise TypeError("URL SBOM was not loaded as dictionary")

                    sbom = cls.parse_obj(sbom_dict)
                    url_ref = UrlFile(url=source)
                    cls.loaded_sboms[url_ref] = sbom
                except (HopprLoadDataError, HTTPError) as ex:
                    raise HopprLoadDataError from ex

        return sbom
