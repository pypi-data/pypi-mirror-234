"""
Base model for Hoppr config files
"""
from __future__ import annotations

import functools
import sys

from typing import Annotated, Any, Callable, ClassVar, Literal, MutableMapping, TypeVar

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import BaseConfig, BaseModel, Extra, Field, create_model, validator
from pydantic_yaml import YamlModel

import hoppr.utils

AnyCycloneDXModel = TypeVar("AnyCycloneDXModel", bound="CycloneDXBaseModel")
UniqueIDMap = Annotated[MutableMapping[str, AnyCycloneDXModel], Field(default={})]

__all__ = []


class HopprMetadata(YamlModel):
    """
    Metadata data model
    """

    name: str
    version: str | int
    description: str


class HopprBaseModel(YamlModel):
    """
    Base Hoppr data model
    """

    class Config(BaseConfig):  # pylint: disable=too-few-public-methods
        """
        Config options for HopprBaseModel
        """

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = Extra.forbid
        use_enum_values = True

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """
        Define to test equality or uniqueness between objects
        """
        return hash(repr(self))


class HopprBaseSchemaModel(HopprBaseModel):
    """
    Base Hoppr config file schema model
    """

    kind: Literal["Credentials", "Manifest", "Transfer"] = Field(..., description="Data model/schema kind")
    metadata: HopprMetadata | None = Field(None, description="Metadata for the file")
    schema_version: str = Field(..., alias="schemaVersion", title="Schema Version")

    @validator("kind", allow_reuse=True, pre=True)
    @classmethod
    def validate_kind(cls, kind: str) -> str:
        """
        Return supplied `kind` value with only first letter capitalized
        """
        return kind.capitalize()


class CycloneDXBaseModel(BaseModel):
    """
    Base CycloneDX data model
    """

    class Config(HopprBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config options for CycloneDXBaseModel"

    # Defining as ClassVar to allow dynamic model creation using custom root types
    deep_merge: ClassVar[bool] = False
    flatten: ClassVar[bool] = False
    observers: ClassVar[dict[object, Callable]] = {}
    unique_id_map: ClassVar[UniqueIDMap]

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other) if isinstance(other, type(self)) else False

    def __hash__(self) -> int:
        return hash(self.unique_id_callback())

    def __init__(self, **data):
        super().__init__(**data)

        unique_id = self.unique_id_callback()
        type(self).unique_id_map[unique_id] = self

    def _has_field(self, field_name: str) -> bool:
        return hasattr(self, field_name) and (getattr(self, field_name) or field_name in list(self.__fields_set__))

    @staticmethod
    def _is_list_of(obj_type: type, field: Any) -> bool:
        """
        Checks if the provided field is a list of the specified type
        """
        return isinstance(field, list) and all(isinstance(item, obj_type) for item in field)

    def _merge_field(self, target_field_name: str, source_field: Any) -> None:
        """
        Merges `source_field` into the field referenced by `target_field_name`
        """
        merged_field = getattr(self, target_field_name)
        field_type = type(merged_field)

        if not self._has_field(target_field_name):
            setattr(self, target_field_name, source_field)
            return

        if isinstance(field_type, type(BaseModel)):
            merged_field = CycloneDXBaseModel.create(model=merged_field)
            source_field = CycloneDXBaseModel.create(model=source_field)
            merged_field.merge(source_field)
        elif self._is_list_of(BaseModel, merged_field):
            merged_field = hoppr.utils.dedup_list([CycloneDXBaseModel.create(model=_field) for _field in merged_field])
            source_field = [CycloneDXBaseModel.create(model=_field) for _field in source_field or []]
            self._merge_field_items(merged_field, source_field)

        setattr(self, target_field_name, merged_field)

    @staticmethod
    def _merge_field_items(target_field: list[CycloneDXBaseModel], source_field: list[CycloneDXBaseModel]) -> None:
        """
        Merges the items from `source_field` into `target_field`
        """
        for source_item in source_field:
            if source_item in target_field:
                merged_item = target_field[target_field.index(source_item)]
                merged_item.merge(source_item)
            else:
                target_field.append(source_item)

    def unique_id_callback(self) -> str:
        """
        Default callback method to get a model object's unique ID
        """
        try:
            callback = {
                "Advisory": lambda obj: obj.url,
                "Annotations": lambda obj: obj.bom_ref or obj.text,
                "Command": lambda obj: obj.executed or repr(self),
                "Commit": lambda obj: obj.uid,
                "Component": lambda obj: obj.bom_ref,
                "ComponentData": lambda obj: obj.bom_ref or repr(self),
                "Copyright": lambda obj: obj.text,
                "Dependency": lambda obj: obj.ref,
                "ExternalReference": lambda obj: f"{obj.type}-{obj.url}",
                "Formula": lambda obj: obj.bom_ref or repr(self),
                "License": lambda obj: obj.id or obj.name or repr(self),
                "LicenseChoice": lambda obj: obj.license or obj.expression or repr(self),
                "Note": lambda obj: obj.text,
                "Occurrence": lambda obj: obj.bom_ref or repr(self),
                "Reference": lambda obj: obj.id,
                "Sbom": lambda obj: obj.serialNumber,
                "Service": lambda obj: obj.bom_ref or f"{obj.name}-{obj.version}",
                "Signer": lambda obj: obj.value,
                "Task": lambda obj: obj.bom_ref or obj.uid,
                "Vulnerability": lambda obj: obj.id or repr(self),
                "Workflow": lambda obj: obj.bom_ref or obj.uid,
                "Workspace": lambda obj: obj.bom_ref or obj.uid,
            }[type(self).__name__]

            return callback(self)
        except KeyError:
            return repr(self)

    @classmethod
    def create(cls: type[AnyCycloneDXModel], model: BaseModel) -> AnyCycloneDXModel:
        """
        Update a BaseModel object with CycloneDXBaseModel attributes and methods

        Args:
            model (BaseModel): The BaseModel object to update

        Returns:
            AnyCycloneDXModel: The updated BaseModel object
        """
        model_cls = cls.make_model(name=type(model).__name__)
        return model_cls(**model.dict(by_alias=True, exclude_none=True, exclude_unset=True))  # pyright: ignore

    @classmethod
    @functools.cache
    def make_model(cls: type[AnyCycloneDXModel], name: str) -> type[AnyCycloneDXModel]:
        """
        Dynamically create a model class suitable for merging

        Args:
            name (str): Name of the existing model

        Returns:
            type[AnyCycloneDXModel]: The generated model class
        """
        # Return explicitly defined models directly
        if name in {"Component", "ExternalReference", "Hash", "Property"}:
            return sys.modules["hoppr.models.sbom"].__dict__[name]

        if name.startswith("License"):
            return sys.modules["hoppr.models.licenses"].__dict__[name]

        if name.startswith("Affect"):
            return sys.modules["hoppr.models.affect"].__dict__[name]

        model_cls = cdx.__dict__[name]

        merge_model = create_model(model_cls.__name__, __base__=(cls, model_cls), __module__=__name__)

        # Set model's pydantic `Config` class and `__hash__` method
        setattr(merge_model, "__config__", cls.Config)

        # Add `unique_id_map` class attribute for caching model objects
        merge_model.__class_vars__.add("unique_id_map")
        merge_model.__annotations__["unique_id_map"] = "ClassVar[UniqueIDMap]"
        setattr(merge_model, "unique_id_map", {})

        # Add updated model to current module and make importable from other modules
        setattr(sys.modules[__name__], merge_model.__name__, merge_model)
        __all__.append(merge_model.__name__)
        merge_model.update_forward_refs()

        return merge_model

    @classmethod
    def find(cls: type[AnyCycloneDXModel], unique_id: str) -> AnyCycloneDXModel | None:
        """
        Look up model object by its unique ID string

        Args:
            unique_id (str): Unique ID string to look up

        Returns:
            AnyCycloneDXModel | None: Model object if found, otherwise None
        """
        return cls.unique_id_map.get(unique_id)

    def merge(self: AnyCycloneDXModel, other: AnyCycloneDXModel) -> None:
        """
        Merge model instance of same type into self

        Args:
            other (AnyCycloneDXModel): Model object to merge
        """
        if (self_type := type(self).__name__) != (other_type := type(other).__name__):
            raise TypeError(f"Type '{other_type}' cannot be merged into '{self_type}'")

        self.notify(data=f"  Merging '{type(self).__qualname__}' attributes...")

        for field_name in self.__fields__:
            self.notify(data=f"    Merging field '{type(self).__qualname__}.{field_name}'...")

            if (source_field := getattr(other, field_name, None)) is None:
                continue

            self._merge_field(field_name, source_field)

    def notify(self, data: str) -> None:
        """
        Call the callback function for all registered subscribers
        """
        for callback in self.observers.values():
            callback(data)

    def subscribe(self, observer: object, callback: Callable) -> None:
        """
        Register an observer
        """
        self.observers[observer] = callback

    def unsubscribe(self, observer: object) -> None:
        """
        Unregister an observer
        """
        self.observers.pop(observer, None)
