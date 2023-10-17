"""
Models to express `Affect.versions` fields
"""
from __future__ import annotations

from typing import Annotated, ClassVar

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import BaseModel, Field

from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap


class AffectVersion(BaseModel):
    """
    AffectVersion data model representing properties of `versions` items
    """

    version: cdx.Version | None = Field(default=None)
    range: cdx.Range | None = Field(default=None)
    status: cdx.AffectedStatus | None = Field(
        default=cdx.AffectedStatus.affected,
        description="The vulnerability status for the version or range of versions.",
    )


class AffectVersionVersionRequired(AffectVersion):
    """
    Affect.versions item model with required `version` field
    """

    version: cdx.Version


class AffectVersionRangeRequired(AffectVersion):
    """
    Affect.versions item model with required `range` field
    """

    range: cdx.Range


AffectVersions = list[AffectVersionVersionRequired | AffectVersionRangeRequired] | None


class Affect(CycloneDXBaseModel, cdx.Affect):
    """
    Affect data model derived from CycloneDXBaseModel with overridden `versions` field
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Affect model"

    versions: Annotated[
        AffectVersions,
        Field(
            description="Zero or more individual versions or range of versions.",
            title="Versions",
        ),
    ] = None

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}
