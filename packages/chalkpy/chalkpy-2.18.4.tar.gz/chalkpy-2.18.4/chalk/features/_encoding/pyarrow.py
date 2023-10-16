from __future__ import annotations

import dataclasses
import decimal
import enum
import ipaddress
import uuid
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, List, Set, Tuple, Type, TypedDict, Union, cast

import attrs
import pyarrow as pa
from pydantic import BaseModel
from typing_extensions import Annotated, get_args, get_origin, is_typeddict

from chalk.features._encoding.primitive import TPrimitive
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import is_namedtuple, unwrap_optional_and_annotated_if_needed
from chalk.utils.enum import get_enum_value_type
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import numpy as np
except:
    np = None

if TYPE_CHECKING:
    import polars as pl

__all__ = ["pyarrow_to_primitive", "pyarrow_to_polars", "rich_to_pyarrow"]


def _is_features_cls(typ: Any) -> bool:
    return getattr(typ, "__chalk_feature_set__", False)


def _is_chalk_dataframe(typ: Any):
    from chalk.features.dataframe import DataFrame

    unwrapped = unwrap_optional_and_annotated_if_needed(typ)
    return isinstance(unwrapped, type) and issubclass(unwrapped, DataFrame)


def rich_to_pyarrow(
    python_type: Type, name: str, in_struct: bool = False, parent_namespaces: Tuple[str] = None
) -> pa.DataType:
    """
    Recursively convert a python type to a PyArrow dtype.
    :param python_type:
    :param name:
    :param in_struct: Whether this function is being called recursively for a member of a struct type.
    Certain datatypes need to be handled differently if nested inside a struct.
    :param parent_namespaces: List of parent namespaces for nested has-ones/has-manys.
    If we run into an infinite loop, skip the field whose namespace we're already in
    (e.g. When serializing Card.customer, skip Card.customer.card....)
    """
    # Polars seems to allow optional for any dtype, so we ignore it when computing dtypes
    python_type = unwrap_optional_and_annotated_if_needed(python_type)
    origin = get_origin(python_type)
    if origin is not None:
        # Handling namedtuples above as structs before tuples, to ensure a namedtuple is not treated like
        # a list
        args = get_args(python_type)
        if origin == Annotated:
            if len(args) < 1:
                raise TypeError(
                    "Annotated types must contain the underlying type as the first argument -- e.g. Annotated[int, 'annotation']"
                )
            return rich_to_pyarrow(args[0], name, in_struct=in_struct, parent_namespaces=parent_namespaces)
        if origin in (list, List, set, Set, frozenset, FrozenSet):
            typ_name = origin.__name__
            if len(args) == 0:
                raise TypeError(
                    f"{typ_name} features must be annotated with the type of the element -- e.g. {typ_name}[int]"
                )
            if len(args) > 1:
                raise TypeError(
                    f"{typ_name} annotations should only take one argument -- e.g. {typ_name}[int]. Instead, got {typ_name}[{', '.join(args)}]"
                )
            arg = args[0]
            return pa.large_list(
                rich_to_pyarrow(arg, name=f"{name}[]", in_struct=in_struct, parent_namespaces=parent_namespaces)
            )
        if origin in (tuple, Tuple):
            if len(args) == 0:
                raise TypeError(
                    "Tuple features must be annotated with the type of the tuple element -- e.g. `Tuple[int, ...]`"
                )
            if len(args) == 2 and args[1] is ...:
                # Treat a variable-sized, homogenous tuple like a list
                arg = args[0]
                return pa.large_list(
                    rich_to_pyarrow(arg, name=f"{name}[]", in_struct=in_struct, parent_namespaces=parent_namespaces)
                )
            raise TypeError(
                (
                    "Tuple features must have a fixed type and be variable-length tuples (e.g. `Tuple[int, ...]`). "
                    " If you would like a fixed-length of potentially different types, used a NamedTuple."
                )
            )
        raise TypeError(f"Unsupported varardic type annotation: {origin}")
    else:
        if python_type in [list]:
            raise TypeError(
                (
                    f"Unable to determine the PyArrow type for field '{name}' with type `{python_type}`. "
                    "List types must be parameterized by their element type, e.g. list[str] or list[int]. "
                )
            )

    from chalk import Windowed

    if isinstance(python_type, Windowed):
        python_type = python_type.kind
    if not isinstance(python_type, type):
        raise TypeError(f"Type annotations must be a type. Instead, got {python_type}.")
    if issubclass(python_type, enum.Enum):
        # For enums, require all members to have the same type
        return rich_to_pyarrow(
            get_enum_value_type(python_type), name, in_struct=in_struct, parent_namespaces=parent_namespaces
        )
    # First, handle the recursive types -- list, tuple, typeddict, namedtuple, dataclass, pydantic model
    if _is_features_cls(python_type):
        parent_namespaces = (parent_namespaces or ()) + (python_type.namespace,)
        annotations = cached_get_type_hints(python_type)
        fields: List[pa.Field] = []
        for field_name, type_annotation in annotations.items():
            if _is_infinitely_recursive_features_class(parent_namespaces, type_annotation):
                continue
            underlying_dtype = rich_to_pyarrow(
                type_annotation, name=f"{name}.{field_name}", in_struct=True, parent_namespaces=parent_namespaces
            )
            # For a @features class, struct field names should include the namespace (i.e. be the root FQN)
            fields.append(pa.field(f"{python_type.namespace}.{field_name}", underlying_dtype))
        return pa.struct(fields)
    elif (
        dataclasses.is_dataclass(python_type)
        or is_namedtuple(python_type)
        or is_typeddict(python_type)
        or attrs.has(python_type)
        or issubclass(python_type, BaseModel)
    ):
        annotations = cached_get_type_hints(python_type)
        fields: List[pa.Field] = []
        for field_name, type_annotation in annotations.items():
            underlying_dtype = rich_to_pyarrow(
                type_annotation, name=f"{name}.{field_name}", in_struct=True, parent_namespaces=parent_namespaces
            )
            fields.append(pa.field(field_name, underlying_dtype))
        return pa.struct(fields)

    if _is_chalk_dataframe(python_type):
        assert python_type.namespace is not None
        parent_namespaces = (parent_namespaces or ()) + (python_type.namespace,)
        column_fields = []
        for col in python_type.columns:
            if _is_infinitely_recursive_features_class(parent_namespaces, col.typ.parsed_annotation):
                continue
            else:
                column_fields.append((col.fqn, col.typ.parsed_annotation))
        pa_fields = [
            pa.field(fqn, rich_to_pyarrow(typ, name=fqn, in_struct=True, parent_namespaces=parent_namespaces))
            for fqn, typ in column_fields
        ]
        return pa.large_list(pa.struct(pa_fields))
    if issubclass(python_type, str):
        return pa.large_utf8()
    if issubclass(python_type, bool):
        return pa.bool_()
    if np and issubclass(python_type, np.bool_):
        return pa.bool_()
    if issubclass(python_type, int):
        return pa.int64()
    if issubclass(python_type, float):
        return pa.float64()
    if issubclass(python_type, datetime):
        return pa.timestamp("us", "UTC")
    if issubclass(python_type, date):
        if in_struct:
            return pa.date32()
        return pa.date64()
    if issubclass(python_type, time):
        return pa.time64("us")
    if issubclass(python_type, timedelta):
        return pa.duration("us")
    if issubclass(python_type, bytes):
        return pa.large_binary()
    if issubclass(python_type, decimal.Decimal):
        # Using a string for decimals, since polars
        # does not support decimal types
        return pa.large_utf8()
    if issubclass(python_type, uuid.UUID):
        return pa.large_utf8()
    if issubclass(python_type, ipaddress.IPv4Address):
        return pa.uint32()
    if issubclass(python_type, ipaddress.IPv6Address):
        return pa.large_utf8()

    raise TypeError(
        (
            f"Unable to determine the PyArrow type for field '{name}' with type `{python_type}`. "
            "Please set the `dtype` attribute when defining the feature"
        )
    )


def pyarrow_to_primitive(pyarrow_typ: pa.DataType, name: str) -> Type[TPrimitive]:
    if pa.types.is_null(pyarrow_typ):
        return cast(Type[TPrimitive], None)
    if pa.types.is_boolean(pyarrow_typ):
        return cast(Type[TPrimitive], bool)
    if pa.types.is_unsigned_integer(pyarrow_typ) or pa.types.is_signed_integer(pyarrow_typ):
        return cast(Type[TPrimitive], int)
    if pa.types.is_floating(pyarrow_typ):
        return cast(Type[TPrimitive], float)
    if pa.types.is_time(pyarrow_typ):
        return cast(Type[TPrimitive], time)
    if pa.types.is_timestamp(pyarrow_typ):
        return cast(Type[TPrimitive], datetime)
    if pa.types.is_date(pyarrow_typ):
        return cast(Type[TPrimitive], date)
    if pa.types.is_duration(pyarrow_typ):
        return cast(Type[TPrimitive], timedelta)
    if (
        pa.types.is_binary(pyarrow_typ)
        or pa.types.is_fixed_size_binary(pyarrow_typ)
        or pa.types.is_large_binary(pyarrow_typ)
    ):
        return cast(Type[TPrimitive], bytes)
    if pa.types.is_string(pyarrow_typ) or pa.types.is_large_string(pyarrow_typ):
        return cast(Type[TPrimitive], str)
    if pa.types.is_list(pyarrow_typ) or pa.types.is_large_list(pyarrow_typ) or pa.types.is_fixed_size_list(pyarrow_typ):
        pyarrow_typ = cast(Union[pa.ListType, pa.LargeListType, pa.FixedSizeListType], pyarrow_typ)
        underlying = pyarrow_typ.value_type
        return cast(Type[TPrimitive], List[pyarrow_to_primitive(underlying, name=f"{name}[]")])
    if pa.types.is_struct(pyarrow_typ):
        pyarrow_typ = cast(pa.StructType, pyarrow_typ)
        # Dynamically making a TypedDict so members will be parsed with the correct types by cattrs
        annotations: Dict[str, Type[TPrimitive]] = {}
        schema = pa.schema(pyarrow_typ)
        for sub_name, sub_typ in zip(schema.names, schema.types):
            annotations[sub_name] = pyarrow_to_primitive(sub_typ, name=f"{name}.{sub_name}")
        typed_dict_cls = TypedDict(f"__chalk_struct__{name}", annotations)  # type: ignore
        return cast(Type[TPrimitive], typed_dict_cls)
    raise TypeError(f"Unsupported PyArrow type {pyarrow_typ} for field {name}")


def _is_infinitely_recursive_features_class(parent_namespaces: Tuple[str, ...], typ: Type) -> bool:
    """
    If a python type is a Features Class, make sure it's not an infinite loop of nested has-manys or has-ones.
    For instance, if there is a has-one relationship between Card and Customer, trying to serialize Card.customer.card
    will lead to an infinite loop.
    :param parent_namespaces: Series of namespaces that contain the current field. For Card.customer.card, this will be ["card", "customer"]
    :param typ: Same format as Feature.typ.parsed_annotation
    :return: True if `typ` is a nested has-one/many and its namespace is one of the parent_namespaces
    """
    if not (_is_chalk_dataframe(typ) or _is_features_cls(typ)):
        return False
    assert typ.namespace is not None
    return typ.namespace in parent_namespaces


def pyarrow_to_polars(pa_type: pa.DataType, name: str | None = None) -> pl.PolarsDataType:
    """Convert a PyArrow data type into a Polars DataType

    Args:
        pa_type: The PyArrow data type
        name: A name, which is printed in error messages
    """
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if pa.types.is_null(pa_type):
        return pl.Null()
    if pa.types.is_boolean(pa_type):
        return pl.Boolean()
    if pa.types.is_int8(pa_type):
        return pl.Int8()
    if pa.types.is_int16(pa_type):
        return pl.Int16()
    if pa.types.is_int32(pa_type):
        return pl.Int32()
    if pa.types.is_int64(pa_type):
        return pl.Int64()
    if pa.types.is_uint8(pa_type):
        return pl.UInt8()
    if pa.types.is_uint16(pa_type):
        return pl.UInt16()
    if pa.types.is_uint32(pa_type):
        return pl.UInt32()
    if pa.types.is_uint64(pa_type):
        return pl.UInt64()
    if pa.types.is_float16(pa_type):
        return pl.Float32()
    if pa.types.is_float32(pa_type):
        return pl.Float32()
    if pa.types.is_float64(pa_type):
        return pl.Float64()
    if pa.types.is_time(pa_type):
        return pl.Time()
    if pa.types.is_timestamp(pa_type):
        pa_type = cast(pa.TimestampType, pa_type)
        assert pa_type.unit in ("ms", "us", "ns")
        return pl.Datetime(pa_type.unit, pa_type.tz)
    if pa.types.is_date(pa_type):
        return pl.Date()
    if pa.types.is_duration(pa_type):
        pa_type = cast(pa.DurationType, pa_type)
        assert pa_type.unit in ("ms", "us", "ns")
        return pl.Duration(pa_type.unit)
    if pa.types.is_binary(pa_type) or pa.types.is_fixed_size_binary(pa_type) or pa.types.is_large_binary(pa_type):
        return pl.Binary()
    if pa.types.is_string(pa_type) or pa.types.is_large_string(pa_type):
        return pl.Utf8()
    if pa.types.is_list(pa_type) or pa.types.is_large_list(pa_type) or pa.types.is_fixed_size_list(pa_type):
        pa_type = cast(Union[pa.ListType, pa.LargeListType, pa.FixedSizeListType], pa_type)
        underlying = pa_type.value_type
        return pl.List(pyarrow_to_polars(underlying, name=f"{name}[]"))
    if pa.types.is_struct(pa_type):
        pa_type = cast(pa.StructType, pa_type)
        schema = pa.schema(pa_type)

        fields = [
            pl.Field(sub_name, pyarrow_to_polars(sub_typ, name=f"{name}.{sub_name}"))
            for sub_name, sub_typ in zip(schema.names, schema.types)
        ]
        return pl.Struct(fields)
    raise TypeError(f"Unsupported PyArrow type {pa_type}" + (f" for field {name}" if name is not None else ""))
