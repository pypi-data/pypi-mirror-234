"""
Generate JSON schema files from pydantic models
"""
from __future__ import annotations

from pathlib import Path

from pydantic_yaml.compat.yaml_lib import yaml_safe_dump

from hoppr.models import CredentialsFile, HopprBaseModel, HopprSchemaModel, ManifestFile, TransferFile


def write_json_schema(filename: str, model_type: type[HopprBaseModel]) -> None:
    """
    Write JSON schema to file
    """
    with Path(filename).open(mode="w+", encoding="utf-8") as json_schema:
        json_schema.write(model_type.schema_json(indent=2))


def write_yaml_schema(filename: str, model_type: type[HopprBaseModel]) -> None:
    """
    Write YAML schema to file
    """
    with Path(filename).open(mode="w+", encoding="utf-8") as yaml_schema:
        yaml_safe_dump(data=model_type.schema(by_alias=True), stream=yaml_schema, default_flow_style=False)


# Write JSON schema files
write_json_schema(filename="hoppr-credentials-schema-v1.json", model_type=CredentialsFile)
write_json_schema(filename="hoppr-manifest-schema-v1.json", model_type=ManifestFile)
write_json_schema(filename="hoppr-transfer-schema-v1.json", model_type=TransferFile)
write_json_schema(filename="hoppr-combined-schema-v1.json", model_type=HopprSchemaModel)

# Write YAML schema files
write_yaml_schema(filename="hoppr-credentials-schema-v1.yml", model_type=CredentialsFile)
write_yaml_schema(filename="hoppr-manifest-schema-v1.yml", model_type=ManifestFile)
write_yaml_schema(filename="hoppr-transfer-schema-v1.yml", model_type=TransferFile)
write_yaml_schema(filename="hoppr-combined-schema-v1.yml", model_type=HopprSchemaModel)
