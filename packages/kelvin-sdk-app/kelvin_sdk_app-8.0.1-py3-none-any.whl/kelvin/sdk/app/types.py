"""Types."""

from __future__ import annotations

import logging
import re
import sys
from enum import IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseConfig, Field, ValidationError, root_validator, validator
from pydantic.generics import GenericModel
from pydantic.main import ErrorWrapper, ModelField
from typing_inspect import get_args

from kelvin.sdk.datatype import Model

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore


T = TypeVar("T")


class SchemaError(Model):
    is_valid: bool = False
    error: str

    def __bool__(self) -> bool:
        return self.is_valid


class Schema(Model):
    title: Optional[str] = None
    description: Optional[str] = None
    examples: Optional[List[Any]] = None


class BoolSchema(Schema):
    data_type: Literal["raw.boolean", "boolean"]

    def check(self, data: Mapping[str, Any]) -> Optional[SchemaError]:
        value = data.get("value")
        if value is None:
            return SchemaError(error="missing value in parameter")

        # try to losslessly convert value
        if not isinstance(value, bool):
            converted = bool(value)
            if converted == value:
                value = converted

        if not isinstance(value, bool):
            return SchemaError(error="non-boolean value in parameter")

        return None


class StringSchema(Schema):
    min_length: Optional[int] = Field(None, alias="minLength")
    max_length: Optional[int] = Field(None, alias="maxLength")
    pattern: Optional[str] = None
    data_type: Literal["raw.text", "string"]

    def check(self, data: Mapping[str, Any]) -> Optional[SchemaError]:
        value = data.get("value")
        if value is None:
            return SchemaError(error="missing value in parameter")

        if not isinstance(value, str):
            return SchemaError(error="non-string value in parameter")

        n = len(value)

        if self.min_length is not None and n < self.min_length:
            return SchemaError(error=f"length {n} below minimum {self.min_length}")
        if self.max_length is not None and n > self.max_length:
            return SchemaError(error=f"length {n} above maximum {self.max_length}")
        if self.pattern and not re.match(self.pattern, value):
            return SchemaError(error=f"{value} did not match {self.pattern}")

        return None


class IntSchema(Schema):
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    data_type: Literal["raw.int32", "raw.uint32"]

    def check(self, data: Mapping[str, Any]) -> Optional[SchemaError]:
        value = data.get("value")
        if value is None:
            return SchemaError(error="missing value in parameter")

        # try to losslessly convert value
        if isinstance(value, float):
            converted = int(value)
            if converted == value:
                value = converted

        if not isinstance(value, int):
            return SchemaError(error="non-integer value in parameter")

        if self.minimum is not None and value < self.minimum:
            return SchemaError(error=f"value {value} below minimum {self.minimum}")
        if self.maximum is not None and value > self.maximum:
            return SchemaError(error=f"value {value} above maximum {self.maximum}")

        return None


class FloatSchema(Schema):
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    data_type: Literal["raw.float32", "raw.float64", "number"]

    def check(self, data: Mapping[str, Any]) -> Optional[SchemaError]:
        value = data.get("value")
        if value is None:
            return SchemaError(error="missing value in parameter")

        # try to losslessly convert value
        if isinstance(value, int):
            value = float(value)

        if not isinstance(value, float):
            return SchemaError(error="non-float value in parameter")

        if self.minimum is not None and value < self.minimum:
            return SchemaError(error=f"value {value} below minimum {self.minimum}")
        if self.maximum is not None and value > self.maximum:
            return SchemaError(error=f"value {value} above maximum {self.maximum}")

        return None


class Parameter(Model):
    name: str
    schema_: Optional[Union[StringSchema, FloatSchema, IntSchema, BoolSchema]] = Field(
        None,
        alias="schema",
        discriminator="data_type",
    )
    data_type: str
    default: Optional[Mapping[str, Any]] = None

    def check(self, data: Any = None) -> Optional[SchemaError]:
        if self.schema_ is None:
            return None

        if data is None:
            data = self.default
            if data is None:
                return SchemaError(error="parameter not provided and default not available")
        elif not isinstance(data, Mapping):
            return SchemaError(error="invalid data type")

        return self.schema_.check(data)

    @root_validator(pre=True)
    def prepare_validation(cls: Parameter, values: Dict[str, Any]) -> Any:
        data_type = values.get("data_type")
        if data_type is not None:
            schema = values.setdefault("schema", {})
            schema["data_type"] = data_type

        return values


class TypedModel(GenericModel, Model, Generic[T]):
    """Typed model."""

    __slots__ = ("_type",)

    _type: T
    _TYPE_FIELD = "type"

    type: str = Field(
        ...,
        name="Type",
        description="Type.",
    )

    @root_validator(pre=True)
    def validate_type(cls: Type[TypedModel], values: Dict[str, Any]) -> Any:  # type: ignore
        """Validate type."""

        fields = cls.__fields__
        aliases = {x.alias: name for name, x in fields.items()}

        type_field = fields[cls._TYPE_FIELD]

        type_name = values.get(cls._TYPE_FIELD, type_field.default)
        if type_name is None:
            return values

        type_names = {*get_args(type_field.type_)}

        if type_name not in type_names:
            return values

        errors: List[ErrorWrapper] = []

        if type_name not in values:
            field_type = fields[aliases[type_name]].type_
            if any(x.required for x in field_type.__fields__.values()):
                errors += [ErrorWrapper(ValueError(f"{type_name!r} missing"), loc=(type_name,))]
            else:
                values[type_name] = {}

        for name in {*values} & type_names:
            if name == type_name:
                continue
            errors += [
                ErrorWrapper(ValueError(f"{name!r} doesn't match type {type_name!r}"), loc=(name,))
            ]

        if errors:
            raise ValidationError(errors, model=cls) from None  # type: ignore

        return values

    def __init__(self, **kwargs: Any) -> None:
        """Initialise typed-model."""

        super().__init__(**kwargs)

        aliases = {x.alias: name for name, x in self.__fields__.items()}

        object.__setattr__(self, "_type", self[aliases[self.type]])

    __iter__: Callable[[], Iterator[str]]  # type: ignore

    @property
    def _(self) -> T:
        """Selected type."""

        return self._type


class LogLevel(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    INFO = logging.INFO
    ERROR = logging.ERROR
    TRACE = logging.ERROR

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None
