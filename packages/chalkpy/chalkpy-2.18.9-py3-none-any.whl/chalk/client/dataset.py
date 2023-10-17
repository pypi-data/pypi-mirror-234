from __future__ import annotations

import base64
import inspect
import json
import os
import uuid
import warnings
from collections import OrderedDict
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union, cast
from urllib.parse import urlparse

import pandas as pd
import requests as requests
from typing_extensions import assert_never

from chalk.client import ChalkBaseException, Dataset, DatasetRevision
from chalk.client.models import (
    ChalkError,
    ColumnMetadata,
    DatasetFilter,
    DatasetRecomputeResponse,
    DatasetResponse,
    DatasetRevisionResponse,
    OfflineQueryContext,
    QueryStatus,
)
from chalk.features import DataFrame, Feature, FeatureWrapper, deserialize_dtype, ensure_feature
from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.features.feature_set import FeatureSetBase
from chalk.features.pseudofeatures import CHALK_TS_FEATURE, ID_FEATURE, OBSERVED_AT_FEATURE, PSEUDONAMESPACE
from chalk.features.tag import BranchId, EnvironmentId
from chalk.utils.collections import get_unique_item
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

    from chalk.client.client_impl import ChalkAPIClientImpl

_DEFAULT_EXECUTOR = ThreadPoolExecutor(16)
_logger = get_logger(__name__)


class ColNameDecoder:
    def decode_col_name(self, col_name: str) -> str:
        if col_name.startswith("__") and col_name.endswith("__"):
            return col_name
        x_split = col_name.split("_")
        if x_split[0] == "ca":
            return "_".join(x_split[1:])
        elif x_split[0] == "cb":
            root_fqn_b32 = x_split[1]
            return base64.b32decode(root_fqn_b32.replace("0", "=").upper()).decode("utf8")
        elif x_split[0] == "cc":
            # Need to implement serialization / deserialization of the state dict
            raise NotImplementedError("Decoding stateful column names are not yet supported")
        else:
            raise ValueError(f"Unexpected identifier: {x_split[0]}")


class DatasetVersion(IntEnum):
    """Format of the parquet file. Used when loading a dataset so that we know what format it is in"""

    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES = 1
    """
    This is the format that bigquery dumps to when specifying an output bucket and output format
    as part of an (async) query job
    The output contains extra columns, and all column names are b32 encoded, because
    bigquery does not support '.' in column names.
    The client will have to decode column names before loading this data
    All data, except for feature times, are json encoded
    """

    DATASET_WRITER = 2
    """This is the format returned by the dataset writer in engine/"""

    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2 = 3
    """
    This format uses separate columns for the observed at and timestamp columns
    The observed at column is the actual timestamp from when the observation was observed,
    whereas the timestamp column is the original timestamp that the user requested
    """

    COMPUTE_RESOLVER_OUTPUT_V1 = 4

    NATIVE_DTYPES = 5
    """This format has feature values decoded with their native data types.
    It does not require json decoding client-side"""

    NATIVE_COLUMN_NAMES = 6
    """This format does not encode column names"""


def _parallel_download(uris: List[str], executor: ThreadPoolExecutor, lazy: bool) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    df_futures: list[Future[pl.LazyFrame] | Future[pl.DataFrame]] = []

    # Filesystem class registration is non-threadsafe, so let's fetch the supported filesystems here
    # to pre-emptively register them.
    if len(uris) > 0 and uris[0].startswith("gs"):
        # importing here because we shouldn't assume that this is present in all cases
        from fsspec import get_filesystem_class

        get_filesystem_class("gs")

    if len(uris) > 0 and uris[0].startswith("s3"):
        # importing here because we shouldn't assume that this is present in all cases
        from fsspec import get_filesystem_class

        get_filesystem_class("s3")

    for uri in uris:
        # New versions of polars.scan_parquet don't use fsspec, and we need to pass explicit storage options here.
        # However, read_parquet still uses fsspec. In any case, we still collect here, so it doesn't really matter.
        #   https://docs.rs/object_store/0.7.0/src/object_store/gcp/mod.rs.html#963-1083
        #   https://docs.rs/object_store/0.7.0/src/object_store/aws/mod.rs.html#963-1083
        df_futures.append(executor.submit(pl.read_parquet, uri))

        # if lazy:
        #     df_futures.append(executor.submit(pl.scan_parquet, uri))
        # else:
        #     df_futures.append(executor.submit(pl.read_parquet, uri))

    dfs = [df.result() for df in df_futures]
    dfs = [x.select(sorted(x.columns)) for x in dfs]
    # Cast the list to be homogenous
    dfs = cast(Union[List[pl.DataFrame], List[pl.LazyFrame]], dfs)
    df = pl.concat(dfs)
    return df


def _load_dataset_from_chalk_writer(uris: List[str]) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    # V1 datasets should contain just a single URI
    # This URI can be read directly
    # We need to filter the features to remove any pseudofeatures
    if len(uris) != 1:
        raise ValueError("v1 datasets should have just a single URI")
    df = pl.read_parquet(uris[0])
    return df


def _decode_column_names(
    column_names: List[str],
    col_name_decoder: ColNameDecoder | None,
) -> Mapping[str, str]:
    ans: Dict[str, str] = {}
    for x in column_names:
        if x.startswith("__"):
            if x in ("__id__", ID_FEATURE.fqn):
                ans[x] = ID_FEATURE.fqn
            elif x in ("__ts__", CHALK_TS_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = CHALK_TS_FEATURE.fqn
            elif x in ("__observed_at__", "__oat__", OBSERVED_AT_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = OBSERVED_AT_FEATURE.fqn
            # Drop all the other metadata columns
            continue
        if col_name_decoder is None:
            feature_name = x
        else:
            feature_name = col_name_decoder.decode_col_name(x)
        if any(feature_name.endswith(f".__{y}__") for y in ("oat", "rat", "observed_at", "replaced_observed_at")):
            # Drop the timestamp metadata from individual features
            continue
        ans[x] = feature_name
    return ans


def _json_decode(x: Optional[str]):
    if x is None:
        return None
    return json.loads(x)


def _load_dataset_bigquery(
    uris: List[str],
    executor: Optional[ThreadPoolExecutor],
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: bool,
    output_id: bool,
    version: DatasetVersion,
    lazy: bool,
    columns: Optional[Sequence[ColumnMetadata]],
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # unused
    # V2 datasets are in multiple files, and have column names encoded
    # due to DB limitations (e.g. bigquery does not support '.' in column names)
    # In addition, the datasets may contain extra columns (e.g. replaced observed at)
    # All values are JSON encoded
    if executor is None:
        executor = _DEFAULT_EXECUTOR
    df = _parallel_download(uris, executor, lazy)
    return _extract_df_columns(df, output_feature_fqns, output_ts, output_id, version, columns)


def to_utc(df: pl.DataFrame, col: str, expr: pl.Expr):
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if col not in df.schema:
        return expr

    dtype = df.schema[col]
    if isinstance(dtype, pl.Datetime):
        if dtype.time_zone is not None:
            return expr.dt.convert_time_zone("UTC")
        else:
            return expr.dt.replace_time_zone("UTC")
    else:
        return expr


def _extract_df_columns(
    df: Union[pl.DataFrame, pl.LazyFrame],
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: bool,
    output_id: bool,
    version: DatasetVersion,
    column_metadata: Optional[Sequence[ColumnMetadata]] = None,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.NATIVE_DTYPES,
        DatasetVersion.NATIVE_COLUMN_NAMES,
    ):
        if version == DatasetVersion.NATIVE_COLUMN_NAMES:
            col_name_decoder = None
        else:
            col_name_decoder = ColNameDecoder()
        decoded_col_names = _decode_column_names(df.columns, col_name_decoder)

        # Select only the columns in decoded_col_names
        df = df.select(list(decoded_col_names.keys()))
        df = df.rename(dict(decoded_col_names))
        if column_metadata is not None:
            col_name_set = {x.feature_fqn for x in column_metadata}
            ordered_cols: list[str] = []
            for c in df.columns:
                if c not in col_name_set:
                    ordered_cols.append(c)
            for x in column_metadata:
                if x.feature_fqn not in ordered_cols and x.feature_fqn in df.columns:
                    ordered_cols.append(x.feature_fqn)
            df = df.select(ordered_cols)

        # Using an OrderedDict so the order will match the order the user set in the
        # output argument
        expected_cols: Dict[str, pl.Expr] = OrderedDict()
        id_col = pl.col(str(ID_FEATURE))
        if output_id:
            # All dataframes have an __id__ column
            expected_cols[str(ID_FEATURE)] = id_col.alias(str(ID_FEATURE))

        ts_col = to_utc(
            df, str(OBSERVED_AT_FEATURE), pl.col(str(OBSERVED_AT_FEATURE)).fill_null(pl.col(str(CHALK_TS_FEATURE)))
        )
        if output_ts:
            # For the ts feature, we want `__oat__` if not null else `__ts__`
            # it is not null; otherwise, we want
            expected_cols[str(CHALK_TS_FEATURE)] = ts_col.alias(str(CHALK_TS_FEATURE))

        if output_feature_fqns is None:
            # If not provided, return all columns, except for the OBSERVED_AT_FEATURE
            # (the REPLACED_OBSERVED_AT was already dropped in _decode_col_names)
            for x in df.columns:
                if x not in expected_cols and not x.startswith(f"{PSEUDONAMESPACE}.") and "chalk_observed_at" not in x:
                    expected_cols[x] = pl.col(x)

        else:
            # Make a best-effort attempt to determine the pkey and ts column fqn from the root namespace
            # of the other features
            root_ns = get_unique_item(
                [x.split(".")[0] for x in df.columns if not x.startswith(f"{PSEUDONAMESPACE}.")], "root_ns"
            )
            ts_feature = None
            pkey_feature = None
            features_cls = None
            if root_ns in FeatureSetBase.registry:
                features_cls = FeatureSetBase.registry[root_ns]
                ts_feature = features_cls.__chalk_ts__
                pkey_feature = features_cls.__chalk_primary__
            for x in output_feature_fqns:
                if features_cls is not None and x in [f.fqn for f in features_cls.features if f.is_has_one]:
                    for col in df.columns:
                        if col.startswith(f"{x}.") and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x == root_ns:
                    for col in df.columns:
                        if col.startswith(root_ns) and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x in expected_cols:
                    continue
                if x in df.columns:
                    if x == str(CHALK_TS_FEATURE):
                        expected_cols[x] = ts_col.alias(x)
                    else:
                        expected_cols[x] = pl.col(x)
                    continue
                if x == str(CHALK_TS_FEATURE) or (ts_feature is not None and x == str(ts_feature)):
                    # The ts feature wasn't returned as the ts feature, but we are able to figure it out from the graph
                    # Alias the ts_col as the ts fqn (or CHALK_TS_FEATURE fqn if that's what was passed in)
                    expected_cols[x] = ts_col.alias(x)
                    continue
                if pkey_feature is not None and x == str(pkey_feature):
                    expected_cols[x] = id_col.alias(x)
                    continue
                else:
                    # We should _never_ hit this as the query should have failed before results are returned
                    # if an invalid feature was requested
                    raise ValueError(f"Feature '{x}' was not found in the results.")

        df = df.select(list(expected_cols.values()))

    elif version == DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1:
        unique_features = set(df.select(pl.col("feature_name").unique()).lazy().collect()["feature_name"].to_list())
        cols = [
            pl.col("value").filter(pl.col("feature_name").eq(fqn)).first().alias(cast(str, fqn))
            for fqn in unique_features
        ]

        df = df.groupby("pkey").agg(cols)
        decoded_stmts = []
        for col in df.columns:
            if col == "pkey":
                continue
            else:
                decoded_stmts.append(
                    pl.col(col).apply(_json_decode, return_dtype=Feature.from_root_fqn(col).converter.polars_dtype)
                )
        df = df.select(decoded_stmts)
        # it might be a good idea to remember that we used to rename this __id__ column to the primary key
        # We also need to remove columns like feature.__oat__ and feature.__rat__
        df = df.select([col for col in df.columns if not col.endswith("__")])
        return df.select(sorted(df.columns))
    elif version != DatasetVersion.DATASET_WRITER:
        raise ValueError(f"Unsupported version: {version}")

    decoded_stmts = []
    feature_name_to_metadata = None if column_metadata is None else {x.feature_fqn: x for x in column_metadata}
    for col, dtype in zip(df.columns, df.dtypes):
        if version in (
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        ):
            # The parquet file is all JSON-encoded except for the ts column. That is, the only datetime column is for the timestamp,
            # and all other columns are strings
            if isinstance(dtype, pl.Datetime):
                # Assuming that the only datetime column is for timestamps
                decoded_stmts.append(to_utc(df, col, pl.col(col)))
            else:
                decoded_stmts.append(pl.col(col).apply(_json_decode, return_dtype=dtype))
        elif version in (DatasetVersion.NATIVE_DTYPES, DatasetVersion.NATIVE_COLUMN_NAMES):
            if column_metadata is None:
                raise ValueError(
                    "The columns must be provided if the dataset type is NATIVE_DTYPES or NATIVE_COLUMN_NAMES"
                )
            # We already decoded the column names so matching against the fqn
            if col == CHALK_TS_FEATURE or col == OBSERVED_AT_FEATURE:
                decoded_stmts.append(to_utc(df, col, pl.col(col)))
            elif col == ID_FEATURE:
                # The pkey is already decoded properly -- it's always an int or str
                decoded_stmts.append(pl.col(col))
            else:
                assert feature_name_to_metadata is not None
                if col not in feature_name_to_metadata:
                    _logger.info(
                        (
                            f"Column '{col}' was included in the dataset but was not returned in the ColumnMetadata. "
                            "This feature might not be casted correctly."
                        )
                    )
                    if isinstance(dtype, pl.Datetime):
                        # It's probably a TS feature
                        decoded_stmts.append(to_utc(df, col, pl.col(col)))
                    else:
                        decoded_stmts.append(pl.col(col))
                else:
                    col_metadata = feature_name_to_metadata[col]
                    polars_dtype = pyarrow_to_polars(deserialize_dtype(col_metadata.dtype), col)
                    # Don't attempt to cast list and struct types -- it probably won't work
                    # Instead, we should load the dataset via pyarrow, rather than via polars
                    col_expr = pl.col(col)
                    if dtype != polars_dtype and not isinstance(polars_dtype, (pl.Struct, pl.List)):
                        col_expr = col_expr.cast(polars_dtype, strict=True)
                    decoded_stmts.append(col_expr)
        else:
            raise ValueError(f"Unsupported version: {version}")
    return df.select(decoded_stmts)


def load_dataset(
    uris: List[str],
    version: Union[DatasetVersion, int],
    output_features: Optional[Sequence[Union[str, Feature, FeatureWrapper, Any]]] = None,
    output_id: bool = True,
    output_ts: bool = True,
    executor: Optional[ThreadPoolExecutor] = None,
    lazy: bool = False,
    columns: Optional[Sequence[ColumnMetadata]] = None,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # Unused
    if not isinstance(version, DatasetVersion):
        try:
            version = DatasetVersion(version)
        except ValueError:
            raise ValueError(
                (
                    f"The dataset version ({version}) is not supported by this installed version of the Chalk client. "
                    "Please upgrade your chalk client and try again."
                )
            )
    if version == DatasetVersion.DATASET_WRITER:
        return _load_dataset_from_chalk_writer(uris)
    output_feature_fqns = (
        None
        if output_features is None
        else [x if isinstance(x, str) else ensure_feature(x).root_fqn for x in output_features]
    )
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1,
        DatasetVersion.NATIVE_DTYPES,
        DatasetVersion.NATIVE_COLUMN_NAMES,
    ):
        return _load_dataset_bigquery(
            uris,
            executor,
            version=version,
            output_feature_fqns=output_feature_fqns,
            output_id=output_id,
            output_ts=output_ts,
            lazy=lazy,
            columns=columns,
        )
    assert_never(version)


class DatasetRevisionImpl(DatasetRevision):
    _hydrated: bool
    _show_progress: bool

    def __init__(
        self,
        revision_id: uuid.UUID,
        environment: EnvironmentId,
        creator_id: str,
        outputs: List[str],
        givens_uri: Optional[str],
        status: QueryStatus,
        filters: DatasetFilter,
        num_partitions: int,
        output_uris: str,
        output_version: int,
        client: ChalkAPIClientImpl,
        num_bytes: Optional[int] = None,
        created_at: Optional[datetime] = None,
        started_at: Optional[datetime] = None,
        terminated_at: Optional[datetime] = None,
        dataset_name: Optional[str] = None,
        dataset_id: Optional[uuid.UUID] = None,
        branch: Optional[BranchId] = None,
        show_progress: bool = False,
    ):
        self.revision_id = revision_id
        self.environment = environment
        self.creator_id = creator_id
        self.outputs = outputs
        self.givens_uri = givens_uri
        self.status = status
        self.filters = filters
        self.num_partitions = num_partitions
        self.output_uris = output_uris
        self.output_version = output_version
        self.num_bytes = num_bytes
        self.created_at = created_at
        self.started_at = started_at
        self.terminated_at = terminated_at
        self.dataset_name = dataset_name
        self.dataset_id = dataset_id
        self._client = client
        self._branch = BranchId(branch) if branch is not None else None
        self._show_progress = show_progress
        self._hydrated = self.status == QueryStatus.SUCCESSFUL

    @property
    def data_as_polars(self) -> pl.LazyFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `DatasetRevision.data_as_polars` is deprecated. Please use the method `DatasetRevision.get_data_as_polars()` instead."
            )
        )
        return self.get_data_as_polars()

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.LazyFrame:
        context = OfflineQueryContext(environment=self.environment)
        self._hydrate(caller_method=inspect.currentframe().f_code.co_name)
        return self._client._await_offline_query_job(
            job_id=self.revision_id,
            outputs=self.outputs,
            lazy=True,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
            branch=self._branch,
        ).lazy()

    def to_polars(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.DataFrame:
        return self.get_data_as_polars(output_id=output_id, output_ts=output_ts).collect()

    def to_polars_lazyframe(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.LazyFrame:
        return self.get_data_as_polars(output_id=output_id, output_ts=output_ts)

    @property
    def data_as_pandas(self) -> pd.DataFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `DatasetRevision.data_as_pandas` is deprecated. Please use the method `DatasetRevision.get_data_as_pandas()` instead."
            )
        )
        return self.get_data_as_pandas()

    def to_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        return self.get_data_as_pandas(output_id=output_id, output_ts=output_ts)

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading pandas DataFrame for DatasetRevision {self.revision_id}")
        self._hydrate(caller_method=inspect.currentframe().f_code.co_name)
        return (
            self._client._await_offline_query_job(
                job_id=self.revision_id,
                outputs=self.outputs,
                lazy=True,
                context=context,
                output_id=output_id,
                output_ts=output_ts,
                branch=self._branch,
            )
            .lazy()
            .collect()
            .to_pandas()
        )

    @property
    def data_as_dataframe(self) -> DataFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `DatasetRevision.data_as_dataframe` is deprecated. Please use the method `DatasetRevision.get_data_as_dataframe()` instead."
            )
        )
        return self.get_data_as_dataframe()

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> DataFrame:
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading Chalk DataFrame for DatasetRevision {self.revision_id}")
        self._hydrate(caller_method=inspect.currentframe().f_code.co_name)
        return DataFrame(
            data=self._client._await_offline_query_job(
                job_id=self.revision_id,
                outputs=self.outputs,
                lazy=True,
                context=context,
                output_id=output_id,
                output_ts=output_ts,
                branch=self._branch,
            )
        )

    def download_data(
        self,
        path: str,
        output_id: bool = False,
        output_ts: bool = False,
        num_executors: Optional[int] = None,
    ) -> None:
        self._hydrate(caller_method=inspect.currentframe().f_code.co_name)
        context = OfflineQueryContext(environment=self.environment)
        urls = self._client._await_offline_query_job(
            job_id=self.revision_id,
            outputs=self.outputs,
            lazy=True,
            context=context,
            urls_only=True,
            output_id=output_id,
            output_ts=output_ts,
            branch=self._branch,
        )
        if num_executors:
            executor = ThreadPoolExecutor(16)
        else:
            executor = _DEFAULT_EXECUTOR

        def _download_data(url: str, directory_path: str):
            r = requests.get(url)
            parse = urlparse(url)
            destination_filepath = "/".join(parse.path.split("/")[4:])
            destination_directory = os.path.join(directory_path, os.path.dirname(destination_filepath))
            os.makedirs(destination_directory, exist_ok=True)
            with open(f"{directory_path}/{destination_filepath}", "wb") as f:
                f.write(r.content)

        futures = (executor.submit(_download_data, url, path) for url in urls)
        for f in futures:
            f.result()

    def get_input_dataframe(self) -> pl.LazyFrame:
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading input DataFrame for DatasetRevision {self.revision_id}")
        return self._client._await_offline_query_input(
            job_id=self.revision_id,
            lazy=True,
            context=context,
            branch=self._branch,
        ).lazy()

    def __repr__(self) -> str:
        if self.dataset_name:
            return f"DatasetRevision(dataset_name='{self.dataset_name}', revision_id='{self.revision_id}', status='{self.status.value}')"
        return f"DatasetRevision(revision_id='{self.revision_id}')"

    def wait_for_completion(self, show_progress: Optional[bool] = None) -> None:
        self._hydrate(show_progress=show_progress)

    def _hydrate(self, show_progress: Optional[bool] = None, caller_method: Optional[str] = None) -> None:
        """
        :param show_progress: Pass `True` to show a progress bar while waiting for the operation to complete.
        :param caller_method: Caller method name. This will be used to display a user-facing message explaining
        the implicit showing of computation progress.
        """
        if self._hydrated:
            return

        should_show_progress = self._show_progress
        if show_progress is not None:
            should_show_progress = show_progress

        self._client._await_operation_completion(
            operation_id=self.revision_id,
            show_progress=should_show_progress,
            caller_method=caller_method,
            environment_id=self.environment,
        )
        dataset = self._client._get_anonymous_dataset(
            revision_id=str(self.revision_id),
            environment=self.environment,
            branch=self._branch,
        )
        completed_revision = dataset.revisions[-1]

        self.outputs = completed_revision.outputs
        self.environment = completed_revision.environment
        self.revision_id = completed_revision.revision_id
        self._branch = completed_revision._branch
        self.terminated_at = completed_revision.terminated_at
        self.started_at = completed_revision.started_at
        self.created_at = completed_revision.created_at
        self.num_bytes = completed_revision.num_bytes
        self.output_version = completed_revision.output_version
        self.output_uris = completed_revision.output_uris
        self.num_partitions = completed_revision.num_partitions
        self.filters = completed_revision.filters
        self.status = completed_revision.status
        self.givens_uri = completed_revision.givens_uri

        self._hydrated = True


class DatasetImpl(Dataset):
    def __init__(
        self,
        is_finished: bool,
        version: int,
        revisions: List[DatasetRevisionImpl],
        client: ChalkAPIClientImpl,
        environment: EnvironmentId,
        dataset_id: Optional[uuid.UUID] = None,
        dataset_name: Optional[str] = None,
        errors: Optional[List[ChalkError]] = None,
    ):
        self.is_finished = is_finished
        self.version = version
        self.revisions = revisions
        self.environment = environment
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.errors = errors
        self._client = client

    @property
    def data_as_polars(self) -> pl.LazyFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `Dataset.data_as_polars` is deprecated. Please use the method `Dataset.get_data_as_polars()` instead."
            )
        )
        return self.get_data_as_polars()

    def to_polars(self, output_id: bool = False, output_ts: bool = False) -> pl.DataFrame:
        return self.get_data_as_polars(output_id=output_id, output_ts=output_ts).collect()

    def to_polars_lazyframe(self, output_id: bool = False, output_ts: bool = False) -> pl.LazyFrame:
        return self.get_data_as_polars(output_id=output_id, output_ts=output_ts)

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.LazyFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
        )

    @property
    def data_as_pandas(self) -> pd.DataFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `Dataset.data_as_pandas` is deprecated. Please use the method `Dataset.get_data_as_pandas()` instead."
            )
        )
        return self.get_data_as_pandas()

    def to_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        return self.get_data_as_pandas(output_id=output_id, output_ts=output_ts)

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_pandas(
            output_id=output_id,
            output_ts=output_ts,
        )

    @property
    def data_as_dataframe(self) -> DataFrame:
        warnings.warn(
            DeprecationWarning(
                "The property `dataset.data_as_dataframe` is deprecated. Please use `dataset.get_data_as_dataframe()` instead."
            )
        )
        return self.get_data_as_dataframe()

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> DataFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_dataframe(
            output_id=output_id,
            output_ts=output_ts,
        )

    def download_data(
        self,
        path: str,
        num_executors: Optional[int] = 16,
    ) -> None:
        return self.revisions[-1].download_data(
            path=path,
            num_executors=num_executors,
        )

    def get_input_dataframe(
        self,
    ) -> pl.LazyFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_input_dataframe()

    def recompute(
        self,
        features: Optional[List[Union[Feature, Any]]] = None,
        branch: Optional[str] = None,
        wait: bool = False,
        show_progress: bool = False,
    ) -> Dataset:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        if self._client._config.branch is None and branch is None:
            raise ValueError("A branch was not provided to the chalk client or as an argument to recompute.")

        recompute_response = self._client._recompute_dataset(
            dataset_name=self.dataset_name,
            dataset_id=self.dataset_id,
            revision_id=self.revisions[-1].revision_id,
            features=features or [],
            branch=branch or self._client._config.branch,
            environment=self.environment,
        )
        if recompute_response.errors:
            raise ChalkBaseException(errors=recompute_response.errors)
        new_revision = dataset_revision_from_response(recompute_response, self._client)
        new_revision._show_progress = show_progress
        self.revisions.append(new_revision)

        if not wait:
            return self

        new_revision.wait_for_completion()
        return self

    def repr_help(self) -> str:
        return "This Dataset is persisted on the server.  Call .get_data_as_*() to retrieve the data. See https://docs.chalk.ai/docs/datasets for more information."

    def repr_header(self) -> str:
        if self.errors and self.dataset_name:
            return f"Dataset(name='{self.dataset_name}', version='{self.version}', errors='{self.errors}')"
        if self.dataset_name:
            return f"Dataset(name='{self.dataset_name}', version='{self.version}')"
        return f"Dataset(name=<unnamed>)"

    def __repr__(self) -> str:
        return "\n".join([self.repr_header(), self.repr_help()])


def dataset_revision_from_response(
    revision: Union[DatasetRevisionResponse, DatasetRecomputeResponse], client: ChalkAPIClientImpl
) -> DatasetRevisionImpl:
    return DatasetRevisionImpl(
        revision_id=revision.revision_id,
        environment=revision.environment_id,
        creator_id=revision.creator_id,
        outputs=revision.outputs,
        givens_uri=revision.givens_uri,
        status=revision.status,
        filters=revision.filters,
        num_partitions=revision.num_partitions,
        output_uris=revision.output_uris,
        output_version=revision.output_version,
        num_bytes=revision.num_bytes,
        client=client,
        created_at=revision.created_at,
        started_at=revision.started_at,
        terminated_at=revision.terminated_at,
        dataset_name=revision.dataset_name,
        dataset_id=revision.dataset_id,
        branch=revision.branch,
    )


def dataset_from_response(response: DatasetResponse, client: ChalkAPIClientImpl) -> DatasetImpl:
    revisions = [dataset_revision_from_response(revision, client) for revision in response.revisions]
    return DatasetImpl(
        is_finished=response.is_finished,
        version=response.version,
        revisions=revisions,
        environment=response.environment_id,
        client=client,
        dataset_id=response.dataset_id,
        dataset_name=response.dataset_name,
        errors=response.errors,
    )
