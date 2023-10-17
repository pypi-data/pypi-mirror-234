"""
Models to express `licenses` fields
"""
from __future__ import annotations

from typing import Annotated, ClassVar

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from hoppr_cyclonedx_models import spdx
from pydantic import Extra, Field

from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap


class License(CycloneDXBaseModel, cdx.License):
    """
    License data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for License model"
        extra = Extra.allow

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseIDRequired(License):
    """
    License data model derived from CycloneDXBaseModel
    """

    # Override to make `id` field required by removing default value
    id: Annotated[
        spdx.LicenseID | None,
        Field(description="A valid SPDX license ID", examples=["Apache-2.0"], title="License ID (SPDX)"),
    ]

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseNameRequired(License):
    """
    License data model derived from CycloneDXBaseModel
    """

    # Override to make `name` field required by removing default value
    name: Annotated[
        str | None,
        Field(
            description="If SPDX does not define the license used, this field may be used to provide the license name",
            examples=["Acme Software License"],
            title="License Name",
        ),
    ]

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseMultipleItem(CycloneDXBaseModel):  # pylint: disable=missing-class-docstring
    license: Annotated[LicenseIDRequired | LicenseNameRequired, Field()]

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseExpressionItem(CycloneDXBaseModel):
    """
    SPDX license expression data model
    """

    expression: Annotated[
        str,
        Field(
            title="SPDX License Expression",
            examples=["Apache-2.0 AND (MIT OR GPL-2.0-only)", "GPL-3.0-only WITH Classpath-exception-2.0"],
        ),
    ]
    bom_ref: Annotated[
        str | None,
        Field(
            title="BOM Reference",
            description=(
                "An optional identifier which can be used to reference the license elsewhere in the BOM. "
                "Every bom-ref MUST be unique within the BOM."
            ),
            alias="bom-ref",
            min_length=1,
        ),
    ] = None

    unique_id_map: ClassVar[UniqueIDMap] = {}


LicenseExpression = Annotated[
    list[LicenseExpressionItem],
    Field(
        title="SPDX License Expression",
        description="A tuple of exactly one SPDX License Expression.",
        min_items=1,
        max_items=1,
    ),
]


LicenseChoice = list[LicenseMultipleItem] | LicenseExpression | None
