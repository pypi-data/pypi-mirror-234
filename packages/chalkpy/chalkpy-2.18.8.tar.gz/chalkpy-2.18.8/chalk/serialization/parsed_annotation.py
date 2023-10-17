from __future__ import annotations

import types
import warnings
from typing import TYPE_CHECKING, FrozenSet, List, Optional, Set, Tuple, Type, TypeVar, Union, cast

from typing_extensions import Annotated, get_args, get_origin

from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collection_type import GenericAlias

try:
    from google.protobuf.message import Message as ProtobufMessage
except ImportError:
    ProtobufMessage = None

if TYPE_CHECKING:
    from chalk.features import Features
    from chalk.streams import Windowed

T = TypeVar("T")
U = TypeVar("U")
JsonValue = TypeVar("JsonValue")


class ParsedAnnotation:
    def __init__(
        self,
        features_cls: Optional[Type[Features]] = None,
        attribute_name: Optional[str] = None,
        *,
        underlying: Optional[Union[type, Annotated, Windowed]] = None,
    ) -> None:
        # Either pass in the underlying -- if it is already parsed -- or pass in the feature cls and attribute name
        self._features_cls = features_cls
        self._attribute_name = attribute_name
        self._is_nullable: Optional[bool] = None
        self._is_dataframe: Optional[bool] = None
        self._collection_type: Optional[GenericAlias] = None
        self._is_scalar: Optional[bool] = None
        self._is_proto: Optional[bool] = None
        self._is_feature_time: Optional[bool] = None
        self._is_primary: Optional[bool] = None
        self._underlying = None
        self._parsed_annotation = None
        if underlying is not None:
            if features_cls is not None and attribute_name is not None:
                raise ValueError("If specifying the underlying, do not specify (features_cls, attribute_name)")
            self._parse_type(underlying)
        elif features_cls is None or attribute_name is None:
            raise ValueError(
                "If not specifying the underlying, then both the (features_cls, attribute_name) must be provided"
            )
        # Store the class and attribute name to later use typing.get_type_hints to
        # resolve any forward references in the type annotations
        # Resolution happens lazily -- after everything is imported -- to avoid circular imports

    @property
    def is_parsed(self) -> bool:
        return self._underlying is not None

    @property
    def annotation(self) -> Union[str, type, Windowed, Annotated]:
        """Return the type annotation, without parsing the underlying type if it is not yet already parsed."""
        if self._parsed_annotation is not None:
            # It is already parsed. Return it.
            return self._parsed_annotation
        assert self._features_cls is not None
        assert self._attribute_name is not None
        return self._features_cls.__annotations__[self._attribute_name]

    @property
    def parsed_annotation(self) -> Union[type, Windowed]:
        """The parsed type annotation. It will be parsed if needed.

        Unlike `.underlying`, parsed annotation contains any container or optional types, such as
        list, dataframe, or Optional.
        """
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._parsed_annotation is not None
        return self._parsed_annotation

    def __str__(self):
        if isinstance(self.annotation, type):
            return self.annotation.__name__
        return str(self.annotation)

    def _parse_annotation(self):
        assert self._features_cls is not None
        assert self._attribute_name is not None
        hints = cached_get_type_hints(self._features_cls, include_extras=True)
        parsed_annotation = hints[self._attribute_name]
        self._parse_type(parsed_annotation)

    def _parse_type(self, annotation: Optional[Union[type, Windowed, Annotated]]):
        from chalk.features import DataFrame, Features

        assert self._parsed_annotation is None, "The annotation was already parsed"
        self._parsed_annotation = annotation
        self._is_document = False
        self._is_proto = False
        self._document_class = None
        self._proto_class = None
        self._is_nullable = False
        self._is_primary = False
        self._is_feature_time = False
        if self._features_cls is not None and self._attribute_name is not None:
            # Return a more helpful error message, since we have context
            error_ctx = f" {self._features_cls.__name__}.{self._attribute_name}"
        else:
            error_ctx = ""
        origin = get_origin(annotation)
        if origin is Annotated:
            args = get_args(annotation)
            if "__chalk_ts__" in args:
                self._is_feature_time = True
            if "__chalk_primary__" in args:
                self._is_primary = True
            if "__chalk_document__" in args:
                self._is_document = True
                self._document_class = args[0]
            annotation = args[0]
            origin = get_origin(annotation)

        if origin in (
            Union,
            getattr(types, "UnionType", Union),
        ):  # using getattr as UnionType was introduced in python 3.10
            args = get_args(annotation)
            # If it's a union, then the only supported union is for nullable features. Validate this
            if len(args) != 2 or (None not in args and type(None) not in args):
                raise TypeError(
                    f"Invalid annotation for feature{error_ctx}: Unions with non-None types are not allowed"
                )
            annotation = args[0] if args[1] in (None, type(None)) else args[1]
            origin = get_origin(annotation)
            doc_args = get_args(annotation)
            if self._is_document:
                self._document_class = annotation
            if "__chalk_document__" in doc_args:
                self._is_document = True
                annotation = doc_args[0]
                self._document_class = annotation
                origin = get_origin(annotation)
            self._is_nullable = True

        # The only allowed collections here are Set, List, or DataFrame
        if origin in (set, Set):
            args = get_args(annotation)
            assert len(args) == 1, "typing.Set takes just one arg"
            annotation = args[0]
            self._collection_type = Set[cast(Type, annotation)]
        if origin in (frozenset, FrozenSet):
            args = get_args(annotation)
            assert len(args) == 1, "typing.FrozenSet takes just one arg"
            annotation = args[0]
            self._collection_type = FrozenSet[cast(Type, annotation)]
        if origin in (tuple, Tuple):
            args = get_args(annotation)
            assert len(args) == 2 and args[1] is ..., "typing.Tuple is only supported if it is homogenous"
            annotation = args[0]
            self._collection_type = FrozenSet[cast(Type, annotation)]
        if origin in (list, List):
            args = get_args(annotation)
            assert len(args) == 1, "typing.List takes just one arg"
            annotation = args[0]
            self._collection_type = List[cast(Type, annotation)]

        self._is_dataframe = False

        if annotation is not None and isinstance(annotation, type) and issubclass(annotation, DataFrame):
            self._is_dataframe = True
            # For features, annotations like DataFrame[User.id] are not allowed
            # Annotations like these are only allowed in resolvers
            # So, error here.
            # if annotation.references_feature_set is None:
            #     raise TypeError("DF has no underlying type")
            annotation = annotation.references_feature_set

        self._is_scalar = annotation is not None and not (
            isinstance(annotation, type) and issubclass(annotation, (Features, DataFrame))
        )

        if self._collection_type is not None and not self._is_scalar:
            raise TypeError(
                (
                    f"Invalid type annotation for feature {error_ctx}: "
                    f"{str(self._collection_type)} must be of scalar types, "
                    f"not {self._parsed_annotation}"
                )
            )
        if self._is_dataframe and self._is_scalar:
            raise TypeError(
                f"Invalid type annotation for feature{error_ctx}: Dataframes must be of Features types, not {self._parsed_annotation}"
            )

        if (
            annotation is not None
            and ProtobufMessage is not None
            and isinstance(annotation, type)
            and issubclass(annotation, ProtobufMessage)
        ):
            self._is_proto = True
            self._proto_class = annotation

        self._underlying = annotation

    @property
    def is_proto(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_proto is not None
        return self._is_proto

    @property
    def is_document(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_document is not None
        return self._is_document

    @property
    def document_class(self) -> type:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._document_class

    @property
    def proto_class(self) -> type:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._proto_class

    @property
    def is_nullable(self) -> bool:
        """Whether the type annotation is nullable."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_nullable is not None
        return self._is_nullable

    @property
    def underlying(self) -> Union[type, Windowed]:
        """The underlying type annotation from the annotation."""
        warnings.warn(
            DeprecationWarning(
                "`feature.typ.underlying` is deprecated. For scalar features, use `feature.converter.rich_type`. "
                "For has-one features, use `feature.joined_class`."
            )
        )
        if self.parsed_annotation is None:
            self._parse_annotation()
        if self._underlying is None:
            raise TypeError("There is no underlying type")
        return self._underlying

    @underlying.setter
    def underlying(self, underlying: Optional[type]):
        self._underlying = underlying

    @property
    def is_windowed(self) -> bool:
        from chalk.streams import Windowed

        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._underlying is not None
        return isinstance(self._underlying, Windowed)

    @property
    def is_features_cls(self) -> bool:
        from chalk.features import Features

        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._underlying is not None
        return isinstance(self._underlying, type) and issubclass(self._underlying, Features)

    @property
    def as_features_cls(self) -> Type[Features]:
        from chalk.features import Features

        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._underlying is not None
        if not (isinstance(self._underlying, type) and issubclass(self._underlying, Features)):
            raise RuntimeError("The underlying is not a features class")
        return self._underlying

    @property
    def is_dataframe(self) -> bool:
        """Whether the type annotation is a dataframe."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_dataframe is not None
        return self._is_dataframe

    @property
    def collection_type(self) -> Optional[GenericAlias]:
        warnings.warn(
            DeprecationWarning(
                "`feature.typ.collection_type` is deprecated. "
                "Instead, convert to rich types via `feature.converter.from_XXX_to_rich` is a list"
            )
        )
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._collection_type

    @property
    def is_scalar(self) -> bool:
        """Whether the type annotation is a scalar type (i.e. not a Features type)."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_scalar is not None
        return self._is_scalar

    @property
    def is_primary(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_primary is not None
        return self._is_primary

    @property
    def is_feature_time(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_feature_time is not None
        return self._is_feature_time
