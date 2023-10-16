from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Union

if TYPE_CHECKING:
    import polars as pl

    from chalk.features import Filter


class Aggregation:
    """A class for refining an aggregation defined by `op`."""

    def __init__(self, col: pl.Expr, fn: Callable[[pl.Expr], pl.Expr]):
        self.col = col
        self.fn = fn
        self.filters: List[Filter] = []

    def where(self, *f: Union[Filter, Any]):
        """Filter the aggregation to apply to only rows where all the filters
        in f are true. If no rows match the filter, the aggregation for the column
        will be null, and the resulting feature type must be a nullable type.

        Parameters
        ----------
        f
            A set of filters to apply to the aggregation.
            Each of the filters must be true to apply the aggregation.

        Returns
        -------
        Aggregation
            The aggregation, allowing you to continue to chain methods.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.sum(User.val).where(User.val > 5)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ null     │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        self.filters.extend(f)
        return self

    def __add__(self, other):
        return self

    def __radd__(self, other):
        return self


class op:
    """Operations for aggregations in `DataFrame`.

    The class methods on this class are used to create
    aggregations for use in `DataFrame.group_by`.
    """

    @classmethod
    def sum(cls, col, *cols) -> Aggregation:
        """Add together the values of `col` and `*cols` in a `DataFrame`.

        Parameters
        ----------
        col
            There must be at least one column to aggregate.
        cols
            Subsequent columns to aggregate.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.sum(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 4.5      │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        import polars as pl

        cols = [col, *[t for t in cols]]
        if len(cols) == 1:
            return Aggregation(pl.col(str(cols[0])), lambda x: x.sum())
        c = pl.col([str(c) for c in cols])
        return Aggregation(c, lambda x: pl.sum(c))

    @classmethod
    def product(cls, col) -> Aggregation:
        """Multiply together the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column to aggregate. Used in `DataFrame.group_by`.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...         User.active: [True, True, False],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={
        ...         User.val: op.product(User.val),
        ...         User.active: op.product(User.active),
        ...      }
        ... )
        ╭─────────┬──────────┬─────────────╮
        │ User.id │ User.val │ User.active │
        ╞═════════╪══════════╪═════════════╡
        │  1      │ 2        │ 1           │
        ├─────────┼──────────┼─────────────┤
        │  3      │ 10       │ 0           │
        ╰─────────┴──────────┴─────────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.product())

    @classmethod
    def max(cls, col) -> Aggregation:
        """Find the maximum of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the maximum value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.max(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 4        │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.max())

    @classmethod
    def min(cls, col) -> Aggregation:
        """Find the minimum of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the minimum value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.min(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 0.5      │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.min())

    @classmethod
    def quantile(cls, col, q: float) -> Aggregation:
        import polars as pl

        assert q >= 0 <= 1, f"Quantile must be between 0 and 1, but given {q}"
        return Aggregation(pl.col(str(col)), lambda x: x.quantile(q))

    @classmethod
    def median(cls, col) -> Aggregation:
        """Find the median of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the median value. In the case of an
            even number of elements, the median is the mean of the two
            middle elements.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.median(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 3        │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.median())

    @classmethod
    def mean(cls, col) -> Aggregation:
        """Find the mean of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the mean value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.mean(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 3        │
        ├─────────┼──────────┤
        │  3      │ 6.5      │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.mean())

    @classmethod
    def std(cls, col) -> Aggregation:
        """Find the standard deviation of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the standard deviation.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.std(User.val)}
        ... )
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.std())

    @classmethod
    def variance(cls, col) -> Aggregation:
        """Find the variance of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the variance.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.variance(User.val)}
        ... )
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.var())

    @classmethod
    def count(cls, col) -> Aggregation:
        """Find the count of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the count.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.count(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 2        │
        ├─────────┼──────────┤
        │  3      │ 1        │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.count())

    @classmethod
    def concat(cls, col, col2, sep: str = "") -> Aggregation:
        """Concatenate the string values of `col` and `col2` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the last value.
        col2
            The column with which to concatenate `col`.
        sep
            The separator to use when concatenating `col` and `col2`.

        Examples
        --------
        >>> from chalk.features import DataFrame
        ... DataFrame(
        ...     [
        ...         User(id=1, val='a'),
        ...         User(id=1, val='b'),
        ...         User(id=3, val='c'),
        ...         User(id=3, val='d'),
        ...     ]
        ... ).group_by(
        ...     group={User.id: User.id},
        ...     agg={User.val: op.concat(User.val)},
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ "ab"     │
        ├─────────┼──────────┤
        │  3      │ "cd"     │
        ╰─────────┴──────────╯
        """
        import polars as pl

        c = pl.col([str(col), str(col2)])
        return Aggregation(c, lambda x: pl.concat_str(c, separator=sep))

    @classmethod
    def concat_str(cls, col, col2, sep: str = "") -> Aggregation:
        """Deprecated. Use `concat` instead."""
        import polars as pl

        c = pl.col([str(col), str(col2)])
        return Aggregation(c, lambda x: pl.concat_str(c, separator=sep))

    @classmethod
    def last(cls, col) -> Aggregation:
        """Find the last value of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the last value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        ... DataFrame(
        ...     [
        ...         User(id=1, val=1),
        ...         User(id=1, val=3),
        ...         User(id=3, val=7),
        ...         User(id=3, val=5),
        ...     ]
        ... ).sort(
        ...     User.amount, descending=True,
        ... ).group_by(
        ...     group={User.id: User.id},
        ...     agg={User.val: op.last(User.val)},
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 1        │
        ├─────────┼──────────┤
        │  3      │ 5        │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.last())

    @classmethod
    def first(cls, col) -> Aggregation:
        """Find the first value of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the first value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        ... DataFrame(
        ...     [
        ...         User(id=1, val=1),
        ...         User(id=1, val=3),
        ...         User(id=3, val=7),
        ...         User(id=3, val=5),
        ...     ]
        ... ).sort(
        ...     User.amount, descending=False
        ... ).group_by(
        ...     group={User.id: User.id},
        ...     agg={User.val: op.last(User.val)},
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 1        │
        ├─────────┼──────────┤
        │  3      │ 5        │
        ╰─────────┴──────────╯
        """
        import polars as pl

        return Aggregation(pl.col(str(col)), lambda x: x.first())
