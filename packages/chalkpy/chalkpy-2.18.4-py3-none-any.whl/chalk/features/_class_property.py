import dataclasses
import functools
from typing import Any, Callable, List, Type, TypeVar, cast

T = TypeVar("T")
V = TypeVar("V")


@dataclasses.dataclass(frozen=True)
class classproperty:
    fget: Callable[[Any], Any]
    bind_to_instances: bool = True
    cached: bool = False


def _cached_getter(
    instance: T,
    *,
    getter: Callable[[T], V],
    cache: List[V],
) -> V:
    if len(cache) == 1:
        return cache[0]
    val = getter(instance)
    cache.append(val)
    return val


def classproperty_support(cls: Type[T]) -> Type[T]:
    """
    Class decorator to add metaclass to our class.
    Metaclass uses to add descriptors to class attributes, see:
    http://stackoverflow.com/a/26634248/1113207
    """

    # From https://stackoverflow.com/questions/3203286/how-to-create-a-read-only-class-property-in-python
    class Meta(type(cls)):
        __chalk_feature_set__ = True

        # This overload important for feature explosion correctness
        def __str__(self):
            return self.namespace

        def __iter__(self):
            for feature in self.features:
                if feature.is_scalar:
                    yield feature

    cls_vars = dict(vars(cls))
    class_prop_names: List[str] = []

    for name, obj in cls_vars.items():
        if isinstance(obj, classproperty):
            # Removing this pseudoproperty that we really want on the metaclass
            if obj.bind_to_instances:
                class_prop_names.append(name)
            delattr(cls, name)
            if obj.cached:
                setattr(
                    Meta,
                    name,
                    property(
                        functools.partial(
                            _cached_getter,
                            getter=obj.fget,
                            cache=[],
                        )
                    ),
                )
            else:
                setattr(Meta, name, property(obj.fget))

    class Wrapper(cast(Type[object], cls), metaclass=Meta):
        def __getattribute__(self, name: str):
            # Bind all cached properties to the metaclass @property
            if name in class_prop_names:
                return getattr(type(self), name)
            return super().__getattribute__(name)

    Wrapper.__name__ = cls.__name__
    Wrapper.__qualname__ = cls.__qualname__
    Wrapper.__module__ = cls.__module__
    Wrapper.__doc__ = cls.__doc__
    Wrapper.__annotations__ = cls.__annotations__

    return cast(Type[T], Wrapper)
