from __future__ import annotations

import functools
import warnings
from typing import TYPE_CHECKING, Any, Generic, Optional, Protocol, Sequence, Type, TypeVar, Union, cast

import pyarrow as pa

from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    _structs_as_objects_feature_json_converter,
    structure_json_to_primitive,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.features._encoding.pyarrow import pyarrow_to_polars, pyarrow_to_primitive, rich_to_pyarrow
from chalk.features._encoding.rich import structure_primitive_to_rich, unstructure_rich_to_primitive
from chalk.utils.collections import unwrap_annotated_if_needed
from chalk.utils.json import TJSON
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)

if TYPE_CHECKING:
    import polars as pl

_TRich = TypeVar("_TRich")
_TRichCo = TypeVar("_TRichCo", covariant=True)
_TRichCon = TypeVar("_TRichCon", contravariant=True)

_TPrim = TypeVar("_TPrim", bound=TPrimitive)
_TPrimCo = TypeVar("_TPrimCo", bound=TPrimitive, covariant=True)
_TPrimCon = TypeVar("_TPrimCon", bound=TPrimitive, contravariant=True)


class MissingValueError(TypeError):
    """Raised when a missing value is encountered and the missing value strategy is set to ``error``."""

    pass


class TEncoder(Protocol[_TPrimCo, _TRichCon]):
    def __call__(self, value: _TRichCon, /) -> _TPrimCo:
        ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo:
        ...


class FeatureConverter(Generic[_TPrim, _TRich]):
    def __init__(
        self,
        name: str,
        is_nullable: bool,
        rich_default: Union[_TRich, Ellipsis] = ...,
        primitive_default: Union[_TPrim, Ellipsis] = ...,
        rich_type: Union[Type[_TRich], Ellipsis] = ...,
        pyarrow_dtype: Optional[pa.DataType[Any]] = None,
        encoder: Optional[TEncoder[_TPrim, _TRich]] = None,
        decoder: Optional[TDecoder[_TPrim, _TRich]] = None,
    ) -> None:
        self._name = name
        self._rich_type = unwrap_annotated_if_needed(rich_type)
        if pyarrow_dtype is None:
            if rich_type is ...:
                raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
            pyarrow_dtype = rich_to_pyarrow(rich_type, name)

        if rich_type is ...:
            if rich_default != ...:
                raise ValueError(
                    "The `rich_default` cannot be used without the `rich_type`. Perhaps specify the `primitive_default` instead?"
                )
            if is_nullable and primitive_default is ...:
                primitive_default = cast(_TPrim, None)

        else:
            if primitive_default != ...:
                raise ValueError(
                    "The `primitive_default` cannot be used when specifying the `rich_type`. Instead, specify the `rich_default`."
                )
            if is_nullable and rich_default is ...:
                rich_default = cast(_TRich, None)

        self._pyarrow_dtype = pyarrow_dtype
        if pa.types.is_struct(pyarrow_dtype) and is_nullable:
            # Structs are never nullable. Their members can be set to null, however.
            warnings.warn(
                UserWarning(
                    (
                        f"Feature '{self._name}' is a nullable struct (e.g. Optional[...]). A `null` value for a struct "
                        "is equivalent to `null` values for each member of the struct. To fix this warning, remove the "
                        "`Optional[...]` annotation for this feature, and instead add `Optional[...]` to each struct member "
                    )
                )
            )
            is_nullable = False
        self._is_nullable = is_nullable
        self._primitive_type = pyarrow_to_primitive(self._pyarrow_dtype, name)
        if rich_type is ...:
            if encoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
            if decoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
        self._encoder = encoder
        self._decoder = decoder
        self._rich_default = rich_default
        if primitive_default is ... and rich_default != ...:
            # The missing value strategy doesn't really matter because rich_default is not missing
            primitive_default = self.from_rich_to_primitive(rich_default, missing_value_strategy="allow")
        self._primitive_default = primitive_default

    def _to_primitive(self, val: _TRich) -> _TPrim:
        if val is None or self._encoder is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                x = unstructure_rich_to_primitive(val)
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}'"
                ) from e
            if x is None and not self._is_nullable:
                raise ValueError(f"Feature '{self._name}' is null, but it cannot be nullable")
            try:
                return cast(_TPrim, structure_primitive_to_rich(x, cast(Type[_TRich], self.primitive_type)))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}"
                ) from e
        return self._encoder(val)

    def _from_prim(self, val: Union[_TPrim, _TRich]) -> _TRich:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        if val is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                val = structure_primitive_to_rich(cast(_TPrim, val), cast(Type[_TRich], self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}'"
                ) from e
        if self._decoder is None:
            try:
                return structure_primitive_to_rich(cast(_TPrim, val), self._rich_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"Could not convert '{val}' to `{self._rich_type}` for feature '{self._name}'") from e
        if isinstance(val, self._rich_type):
            return cast(_TRich, val)
        return self._decoder(cast(_TPrim, val))

    def from_rich_to_pyarrow(
        self,
        values: Sequence[Union[_TRich, ellipsis, None]],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        prim_values = [self.from_rich_to_primitive(x, missing_value_strategy) for x in values]
        return self.from_primitive_to_pyarrow(prim_values)

    def from_rich_to_primitive(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> _TPrim:
        # Ensure that the rich value is indeed the rich type
        # For example, if a string is passed in for a datetime value, convert it into a datetime
        if self.is_value_missing(value):
            if missing_value_strategy == "allow":
                warnings.warn(UserWarning(f"Allowing missing value for feature '{self._name}' with strategy 'allow'"))
                return cast(_TPrim, value)
            elif missing_value_strategy in ("default_or_error", "default_or_allow"):
                if self.has_default:
                    return self.primitive_default
                elif missing_value_strategy == "default_or_error":
                    raise TypeError(
                        f"The value for feature '{self._name}' is missing, and this feature has no default value."
                    )
                else:
                    warnings.warn(
                        UserWarning(
                            f"Allowing missing value for feature '{self._name}' with strategy 'default_or_allow'"
                        )
                    )
                    return cast(_TPrim, value)
            elif missing_value_strategy == "error":
                raise MissingValueError(
                    f"The value for feature '{self._name}' is missing, but `replace_missing_with_defaults` was set to False."
                )
            else:
                raise ValueError(
                    (
                        f"Unsupported missing value strategy: {missing_value_strategy}. "
                        "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
                    )
                )
        value = self.from_primitive_to_rich(cast(_TPrim, value))
        return self._to_primitive(value)

    def from_rich_to_json(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = FeatureEncodingOptions(),
    ) -> TJSON:
        prim_val = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(prim_val, options=options)

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[_TRich]:
        return [self.from_primitive_to_rich(x) for x in values.to_pylist()]

    def from_pyarrow_to_json(
        self, values: Union[pa.Array, pa.ChunkedArray], options: FeatureEncodingOptions = FeatureEncodingOptions()
    ) -> Sequence[TJSON]:
        return [self.from_primitive_to_json(x, options=options) for x in self.from_pyarrow_to_primitive(values)]

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[_TPrim]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: Union[_TPrim, _TRich]) -> _TRich:
        return self._from_prim(value)

    def from_primitive_to_pyarrow(self, value: Sequence[_TPrim]) -> Union[pa.Array, pa.ChunkedArray]:
        x = pa.array([None if x is ... else x for x in value], type=self._pyarrow_dtype)
        return x

    def from_primitive_to_json(
        self, value: TPrimitive, options: FeatureEncodingOptions = FeatureEncodingOptions()
    ) -> TJSON:
        if options.encode_structs_as_objects:
            return _structs_as_objects_feature_json_converter.unstructure_primitive_to_json(value)
        else:
            return unstructure_primitive_to_json(value)

    def from_json_to_rich(self, value: TJSON) -> _TRich:
        prim_val = self.from_json_to_primitive(value)
        return self.from_primitive_to_rich(prim_val)

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        primitive_vals = [cast(_TPrim, self.from_json_to_primitive(x)) for x in values]
        return self.from_primitive_to_pyarrow(primitive_vals)

    def from_json_to_primitive(self, value: Union[TJSON, TPrimitive]) -> _TPrim:
        try:
            return cast(_TPrim, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`") from e

    @property
    def pyarrow_dtype(self):
        return self._pyarrow_dtype

    @property
    def rich_type(self) -> Type[_TRich]:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        return self._rich_type

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return self._primitive_type

    @functools.cached_property
    def polars_dtype(self) -> pl.PolarsDataType:
        return pyarrow_to_polars(self.pyarrow_dtype, self._name)

    @property
    def has_default(self):
        # primitive default is set <==> rich default is also set or no rich type was provided
        return self._primitive_default != ...

    @property
    def rich_default(self) -> _TRich:
        if self._rich_default is ...:
            raise ValueError(f"Feature '{self._name}' has no default value")
        return self._rich_default

    @property
    def primitive_default(self) -> _TPrim:
        if self._primitive_default is ...:
            raise ValueError(f"Feature '{self._name}' has no default value")
        return self._primitive_default

    def is_value_missing(self, value: Any):
        """Returns whether the ``value`` should be treated as a "missing" value"""
        if value is ...:
            # Ellipsis is always missing
            return True
        if value is None:
            # All nullable args have a default (``None`` if not otherwise specified)
            if pa.types.is_struct(self.pyarrow_dtype):
                # Nones are not missing for structs
                return False
            return not self._is_nullable
        return False

    def is_rich_valid(self, value: _TRich):
        """Returns true if value has a valid rich type"""
        try:
            prim = self.from_rich_to_primitive(value, "default_or_error")
            pa.scalar(prim, type=self.pyarrow_dtype)
            return True
        except (TypeError, ValueError):
            return False
