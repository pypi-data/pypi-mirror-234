from typing import TYPE_CHECKING, Any

from chalk.features.dataframe._filters import convert_filters_to_pl_expr

if TYPE_CHECKING:

    from chalk.features.dataframe._impl import DataFrame as _DataFrameImpl

    class DataFrame(_DataFrameImpl):
        def __class_getitem__(cls, item: Any) -> "DataFrame":
            ...

else:
    from chalk.features.dataframe._impl import DataFrame, DataFrameMeta

    # Reexporting DataFrameMeta for backwards compatability

__all__ = ["DataFrame", "convert_filters_to_pl_expr"]
