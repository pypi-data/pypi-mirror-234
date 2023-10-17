import warnings
from typing import Any, Dict, Tuple, Union

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.filter import Filter
from chalk.features.underscore import (
    SUPPORTED_UNDERSCORE_OPS_BINARY,
    SUPPORTED_UNDERSCORE_OPS_UNARY,
    Underscore,
    UnderscoreAttr,
    UnderscoreBinaryOp,
    UnderscoreCall,
    UnderscoreItem,
    UnderscoreRoot,
    UnderscoreUnaryOp,
)
from chalk.utils.collections import ensure_tuple


def parse_underscore_in_context(exp: Underscore, context: Any, is_pydantic: bool = False) -> Any:
    """
    Parse a (potentially underscore) expression passed in under some "context".
    """
    return _parse_underscore_in_context(
        exp=exp,
        context=context,
        is_pydantic=is_pydantic,
    )


def _parse_underscore_in_context(exp: Any, context: Any, is_pydantic: bool) -> Any:
    # Features of the dataframe are to be written as a dictionary of the fqn split up mapped to
    # the original features. The dictionary is represented immutably here.
    if not isinstance(exp, Underscore):
        # Recursive call hit non-underscore, deal with later
        return exp

    elif isinstance(exp, UnderscoreRoot):
        return context

    elif isinstance(exp, UnderscoreAttr):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        attr = exp._chalk__attr
        from chalk.features.dataframe import DataFrame

        if isinstance(parent_context, DataFrame) and is_pydantic:
            if attr not in parent_context._underlying.schema:
                warnings.warn(
                    f"Attribute {attr} not found in dataframe schema. Returning None. " f"Found expression {exp}."
                )
                return None

            return attr
        else:
            return getattr(parent_context, attr)

    elif isinstance(exp, UnderscoreItem):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        key = exp._chalk__key
        return parent_context[key]

    elif isinstance(exp, UnderscoreCall):
        raise NotImplementedError(
            f"Calls on underscores in DataFrames is currently unsupported. Found expression {exp}"
        )

    elif isinstance(exp, UnderscoreBinaryOp):
        if exp._chalk__op in SUPPORTED_UNDERSCORE_OPS_BINARY:
            left = _parse_underscore_in_context(exp=exp._chalk__left, context=context, is_pydantic=is_pydantic)
            right = _parse_underscore_in_context(exp=exp._chalk__right, context=context, is_pydantic=is_pydantic)
            return eval(f"left {exp._chalk__op} right")

    elif isinstance(exp, UnderscoreUnaryOp):
        if exp._chalk__op in SUPPORTED_UNDERSCORE_OPS_UNARY:
            operand = _parse_underscore_in_context(exp=exp._chalk__operand, context=context, is_pydantic=is_pydantic)
            return eval(f"{exp._chalk__op} operand")

    raise NotImplementedError(f"Unrecognized underscore expression {exp}")
