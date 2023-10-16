import inspect
import logging
from typing import Any, Callable, Iterable, Optional, Set, Tuple, Union, overload

from typing_extensions import TypeAlias

from chalk.features.tag import Environments
from chalk.utils.collections import ensure_tuple

HookFn: TypeAlias = Callable[[], Any]


def _run_all_hooks(environment: str, hooks: Iterable["Hook"]) -> None:
    for hook in hooks:
        if hook.environment is None or environment in hook.environment:
            try:
                hook()
            except Exception as e:
                logging.error(f"Error running hook {hook.fn.__name__}")
                raise e


class Hook:
    # Registry
    before_all: Set["Hook"] = set()
    after_all: Set["Hook"] = set()

    environment: Optional[Tuple[str, ...]]
    fn: HookFn
    filename: str

    def __init__(self, fn: HookFn, filename: str, environment: Optional[Environments] = None):
        self.fn = fn
        self.filename = filename
        self.environment = None if environment is None else ensure_tuple(environment)

    def __call__(self):
        return self.fn()

    def __repr__(self):
        return f'Hook(filename={self.filename}, fn={self.fn.__name__}", environment={str(self.environment)})'

    @classmethod
    def run_all_before_all(cls, environment: str) -> None:
        return _run_all_hooks(environment, cls.before_all)

    @classmethod
    def run_all_after_all(cls, environment: str) -> None:
        return _run_all_hooks(environment, cls.after_all)


@overload
def before_all(fn: HookFn, /) -> Hook:
    ...


@overload
def before_all(fn: None = None, /, environment: Optional[Environments] = None) -> Callable[[HookFn], Hook]:
    ...


def before_all(
    fn: Optional[HookFn] = None, /, environment: Optional[Environments] = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    caller_filename = inspect.stack()[1].filename

    def decorator(f: HookFn):
        hook = Hook(fn=f, filename=caller_filename, environment=environment)
        Hook.before_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator


@overload
def after_all(fn: HookFn, /, environment: Optional[Environments] = None) -> Hook:
    ...


@overload
def after_all(fn: None = None, /, environment: Optional[Environments] = None) -> Callable[[HookFn], Hook]:
    ...


def after_all(
    fn: Optional[HookFn] = None, /, environment: Optional[Environments] = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    caller_filename = inspect.stack()[1].filename

    def decorator(f: HookFn):
        hook = Hook(fn=f, filename=caller_filename, environment=environment)
        Hook.after_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator
