import os
import sys
from pathlib import Path
from typing import Any, List, Optional


def get_classpath(x: object) -> Path:
    filepath = sys.modules[x.__module__].__file__
    assert filepath is not None
    return Path(os.path.abspath(filepath))


def get_classpath_or_name(x: Any) -> str:
    module = sys.modules[x.__module__]
    return getattr(module, "__file__", None) or getattr(module, "__name__")


def get_directory_root() -> Optional[Path]:
    current = Path(os.path.dirname(os.path.abspath("dummy.txt")))
    while True:
        if any((current / f).exists() for f in ("chalk.yaml", "chalk.yml")):
            return current
        if Path(os.path.dirname(current)) == current:
            # This is '/'
            return None
        current = current.parent


def _search_recursively_for_file(base: Path, filename: str) -> List[Path]:
    ans = []
    assert base.is_dir()
    while True:
        filepath = base / filename
        if filepath.exists():
            ans.append(filepath)
        parent = base.parent
        if parent == base:
            return ans
        base = parent
