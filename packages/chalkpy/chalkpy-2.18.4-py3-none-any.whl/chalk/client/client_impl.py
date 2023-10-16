from __future__ import annotations

import base64
import collections.abc
import itertools
import json
import os
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Literal, Mapping, Optional, Sequence, Type, TypeVar, Union, cast, overload
from urllib.parse import urljoin

import pandas as pd
import requests
from dateutil import parser
from pydantic import ValidationError
from pydantic.main import BaseModel
from requests import HTTPError
from requests import JSONDecodeError as RequestsJSONDecodeError
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from chalk._reporting.models import BatchReport, BatchReportResponse
from chalk._reporting.progress import ProgressService
from chalk._version import __version__ as chalkpy_version
from chalk.client import ChalkClient, FeatureReference, OnlineQueryResult
from chalk.client.dataset import DatasetImpl, DatasetVersion, dataset_from_response, load_dataset
from chalk.client.exc import _CHALK_TRACE_ID_KEY, ChalkAuthException, ChalkBaseException, ChalkCustomException
from chalk.client.models import (
    BranchDeployRequest,
    BranchDeployResponse,
    BranchIdParam,
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    ChalkError,
    ComputeResolverOutputRequest,
    ComputeResolverOutputResponse,
    CreateOfflineQueryJobRequest,
    CreateOfflineQueryJobResponse,
    DatasetRecomputeRequest,
    DatasetRecomputeResponse,
    DatasetResponse,
    ErrorCode,
    ExchangeCredentialsRequest,
    ExchangeCredentialsResponse,
    FeatureDropRequest,
    FeatureDropResponse,
    FeatureObservationDeletionRequest,
    FeatureObservationDeletionResponse,
    FeatureResult,
    GetOfflineQueryJobResponse,
    OfflineQueryContext,
    OfflineQueryInput,
    OnlineQuery,
    OnlineQueryContext,
    OnlineQueryManyRequest,
    OnlineQueryRequest,
    OnlineQueryResponse,
    OnlineQueryResponseFeather,
    OnlineQueryResultFeather,
    QueryMeta,
    ResolverRunResponse,
    StreamResolverTestMessagePayload,
    StreamResolverTestRequest,
    StreamResolverTestResponse,
    TriggerResolverRunRequest,
    UpdateGraphEntityResponse,
    WhoAmIResponse,
)
from chalk.client.serialization.query_serialization import (
    MULTI_QUERY_MAGIC_STR,
    _decode_multi_query_responses,
    _write_query_to_buffer,
)
from chalk.config.auth_config import load_token
from chalk.config.project_config import load_project_config
from chalk.features import DataFrame, Feature, FeatureNotFoundException, FeatureWrapper, ensure_feature, unwrap_feature
from chalk.features._encoding.inputs import recursive_encode_inputs
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.features.resolver import Resolver
from chalk.features.tag import BranchId, EnvironmentId
from chalk.parsed.branch_state import BranchGraphSummary
from chalk.utils import notebook
from chalk.utils.constants import _EMPTY
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

_logger = get_logger(__name__)

T = TypeVar("T")


class _ChalkHTTPException(BaseModel):
    detail: str
    trace: Optional[str] = None
    errors: Optional[List[ChalkError]] = None


class _ChalkClientConfig(BaseModel):
    name: str
    client_id: str
    client_secret: str
    api_server: str
    query_server: str
    active_environment: Optional[str] = None
    branch: Optional[BranchId] = None


class _BranchDeploymentInfo(BaseModel):
    deployment_id: str
    created_at: datetime


class _BranchInfo(BaseModel):
    name: str
    latest_deployment: Optional[str]
    latest_deployment_time: Optional[datetime]
    deployments: List[_BranchDeploymentInfo]


class _BranchMetadataResponse(BaseModel):
    branches: List[_BranchInfo]

    def __str__(self):
        def _make_line(info: _BranchInfo) -> str:
            latest_str = ""
            if info.latest_deployment_time and info.latest_deployment_time:
                latest_str = f" -- latest: {info.latest_deployment_time.isoformat()} ({info.latest_deployment})"
            return f"* `{info.name}`:\t{len(info.deployments)} deployments" + latest_str

        return "\n".join(_make_line(bi) for bi in self.branches)


def _validate_offline_query_inputs(
    inputs: Mapping[Union[str, Feature, Any], Any]
) -> Mapping[Union[str, Feature, Any], Any]:
    if len(inputs) == 0:
        return inputs

    def _is_scalar(v):
        return not isinstance(v, collections.abc.Iterable) or isinstance(v, str)

    scalar_values = {k: v for (k, v) in inputs.items() if _is_scalar(v)}
    if len(scalar_values) == len(inputs):
        return {str(k): [v] for (k, v) in inputs.items()}
    elif len(scalar_values) > 0:
        first_key = next(iter(scalar_values.keys()))
        error_msg = (
            f"Failed to parse query inputs: offline_query() expects multiple input values for each feature. "
            f"Found a single value of type {type(inputs[first_key])} for key '{str(first_key)}'."
        )
        raise ValueError(error_msg)
    else:
        return {str(k): v for (k, v) in inputs.items()}


def _to_offline_query_input(
    input: Union[Mapping[Union[str, Feature, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame],
    input_times: Union[Sequence[datetime], datetime, None],
) -> OfflineQueryInput:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(input, (DataFrame, pl.DataFrame)):
        input = input.to_pandas()
    if isinstance(input, collections.abc.Mapping):
        input = _validate_offline_query_inputs(input)
    pd_dataframe: pd.DataFrame
    if isinstance(input, pd.DataFrame):
        pd_dataframe = input
    else:
        pd_dataframe = pd.DataFrame(input)

    columns = pd_dataframe.columns
    matrix: List[List[Any]] = pd_dataframe.T.values.tolist()

    columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]
    if input_times is None:
        input_times = datetime.now(timezone.utc)
    if isinstance(input_times, datetime):
        input_times = [input_times for _ in range(len(pd_dataframe))]
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo

    input_times = [x.replace(tzinfo=local_tz) if x.tzinfo is None else x for x in input_times]
    input_times = [x.astimezone(timezone.utc) for x in input_times]

    matrix.append([a for a in input_times])

    for col_index, column in enumerate(matrix):
        for row_index, value in enumerate(column):
            try:
                f = Feature.from_root_fqn(columns_fqn[col_index])
            except FeatureNotFoundException:
                # The feature is not in the graph, so passing the value as-is and hoping it's possible
                # to json-serialize it
                encoded_feature = value
            else:
                encoded_feature = f.converter.from_rich_to_json(
                    value,
                    missing_value_strategy="error",
                )

            matrix[col_index][row_index] = encoded_feature

    return OfflineQueryInput(
        columns=columns_fqn,
        values=matrix,
    )


class OnlineQueryResponseImpl(OnlineQueryResult):
    data: List[FeatureResult]
    errors: List[ChalkError]
    warnings: List[str]
    meta: Optional[QueryMeta]

    def __init__(
        self,
        data: List[FeatureResult],
        errors: List[ChalkError],
        warnings: List[str],
        meta: Optional[QueryMeta] = None,
    ):
        self.data = data
        self.errors = errors
        self.warnings = warnings
        self.meta = meta
        import math

        for d in self.data:
            if isinstance(d.value, float) and math.isnan(d.value):
                d.value = None
            if d.value is not None:
                try:
                    f = Feature.from_root_fqn(d.field)
                except FeatureNotFoundException:
                    self.warnings.append(
                        f"Return data {d.field}:{d.value} cannot be decoded. Attempting to JSON decode"
                    )
                else:
                    if f.is_has_many:
                        # Has-manys are returned by the server in a columnar format, i.e.:
                        # {"columns": ["book.id", "book.title"], "values": [[1, 2], ["Dune", "Children of Dune"]]}
                        # FeatureConverter expects a list of structs, i.e.:
                        # [{"book.id": 1, "book.title": "Dune"}, {"book.id": 2, "book.title": "Children of Dune"}]
                        cols = d.value["columns"]
                        vals = d.value["values"]
                        vals_flattened = list(zip(*vals))
                        value = [{k: v for k, v in zip(cols, row)} for row in vals_flattened]
                    else:
                        value = d.value
                    d.value = f.converter.from_json_to_rich(value)

        self._values = {d.field: d for d in self.data}

    def _df_repr(self):
        info = []
        for x in self.data:
            if isinstance(x.value, pd.DataFrame):
                info.append({"Feature": x.field, "Value": f"DataFrame[shape={x.value.shape}]"})
            elif isinstance(x.value, DataFrame):
                value_repr = f"DataFrame[shape={x.value.shape}]"
                info.append({"Feature": x.field, "Value": value_repr})
            elif isinstance(x.value, Enum):
                info.append({"Feature": x.field, "Value": x.value.value})
            else:
                info.append({"Feature": x.field, "Value": x.value})
        return info

    def __repr__(self) -> str:
        lines = []
        for e in self.errors:
            nice_code = str(e.code.value).replace("_", " ").capitalize()
            # {str(e.category.value).capitalize()}
            lines.append(
                f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
            )
            lines.append(e.message)
            lines.append("")

            metadata = {
                "Exception Kind": e.exception and e.exception.kind,
                "Exception Message": e.exception and e.exception.message,
                "Stacktrace": e.exception and e.exception.stacktrace,
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            for k, v in metadata.items():
                lines.append(f"*{k}*")
                lines.append(f"")
                lines.append(v)
        errs = "\n".join(lines)

        return repr(pd.DataFrame(self._df_repr())) + "\n" + errs

    def __str__(self):
        lines = []
        for e in self.errors:
            nice_code = str(e.code.value).replace("_", " ").capitalize()
            # {str(e.category.value).capitalize()}
            lines.append(
                f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
            )
            lines.append(e.message)
            lines.append("")

            metadata = {
                "Exception Kind": e.exception and e.exception.kind,
                "Exception Message": e.exception and e.exception.message,
                "Stacktrace": e.exception and e.exception.stacktrace,
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            for k, v in metadata.items():
                lines.append(f"*{k}*")
                lines.append(f"")
                lines.append(v)
        errs = "\n".join(lines)
        return str(pd.DataFrame(self._df_repr())) + "\n" + errs

    def _repr_markdown_(self):
        lines = []
        if len(self.errors) > 0:
            lines.append(f"## {len(self.errors)} Errors")
            lines.append("")
            for e in self.errors:
                nice_code = str(e.code.value).replace("_", " ").capitalize()
                # {str(e.category.value).capitalize()}
                lines.append(
                    f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
                )
                lines.append(e.message)
                lines.append("")

                metadata = {
                    "Exception Kind": e.exception and e.exception.kind,
                    "Exception Message": e.exception and e.exception.message,
                    "Stacktrace": e.exception and e.exception.stacktrace,
                }
                metadata = {k: v for k, v in metadata.items() if v is not None}
                for k, v in metadata.items():
                    lines.append(f"*{k}*")
                    lines.append(f"")
                    lines.append(v)

        if len(self.data) > 0:
            import polars as pl

            lines.append("")
            lines.append(f"## Features")
            lines.append("```")
            content = str(pl.DataFrame(self._df_repr()))
            split = content.split("\n")
            main = "\n".join(itertools.chain(split[1:3], split[5:]))
            lines.append(main)
            lines.append("```")

        return "\n".join(lines)

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(str(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value


class ChalkAPIClientImpl(ChalkClient):
    __name__ = "ChalkClient"
    __qualname__ = "chalk.client.ChalkClient"

    _latest_client: Optional[ChalkAPIClientImpl] = None

    def __repr__(self):
        branch_text = ""
        if self._config.branch is not None:
            branch_text = f", branch='{self._config.branch}'"
        return f"chalk.client.ChalkClient<{self._config.name}{branch_text}>"

    def __new__(cls, *args: Any, **kwargs: Any) -> ChalkClient:
        obj = object.__new__(ChalkAPIClientImpl)
        return obj

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        query_server: Optional[str] = None,
        branch: Optional[BranchId] = None,
        _skip_cache: bool = False,
        session: Optional[requests.Session] = None,
        additional_headers: Optional[Mapping[str, str]] = None,
    ):
        self.session: requests.Session = session or requests.Session()

        if session is None:
            retries = Retry(connect=3, read=3)
            self.session.mount("https://", HTTPAdapter(max_retries=retries))
            self.session.mount("http://", HTTPAdapter(max_retries=retries))

        token = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=_skip_cache,
        )
        if token is None:
            raise ChalkAuthException()

        api_server = token.apiServer or "https://api.chalk.ai"
        self._config = _ChalkClientConfig(
            name=token.name or "",
            client_id=token.clientId,
            client_secret=token.clientSecret,
            api_server=api_server,
            query_server=query_server or api_server,
            branch=branch,
            active_environment=token.activeEnvironment,
        )

        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"chalkpy-{chalkpy_version}",
            "X-Chalk-Client-Id": self._config.client_id,
            "X-Chalk-Features-Versioned": "true",
        }
        self._default_headers.update(additional_headers or {})

        self._exchanged_credentials = False
        self._primary_environment = None

        self.__class__._latest_client = self
        if notebook.is_notebook():
            if branch is None:
                self.whoami()
            else:
                self._load_branches()

    def _exchange_credentials(self):
        _logger.debug("Performing a credentials exchange")
        resp = self.session.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=60,
        )
        resp.raise_for_status()
        response_json = resp.json()
        try:
            creds = ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response=resp)
        self._default_headers["Authorization"] = f"Bearer {creds.access_token}"
        self._primary_environment = creds.primary_environment
        self._exchanged_credentials = True

    def _get_headers(
        self,
        environment_override: Optional[str],
        preview_deployment_id: Optional[str],
        branch: Optional[Union[BranchId, _EMPTY]],
    ) -> dict[str, str]:
        x_chalk_env_id = environment_override or self._config.active_environment or self._primary_environment
        headers = dict(self._default_headers)  # shallow copy
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id
        if preview_deployment_id is not None:
            headers["X-Chalk-Preview-Deployment"] = preview_deployment_id

        if branch is _EMPTY:
            pass
        elif branch is not None:
            headers["X-Chalk-Branch-Id"] = branch
        elif self._config.branch is not None:
            headers["X-Chalk-Branch-Id"] = self._config.branch

        return headers

    @staticmethod
    def _raise_if_200_with_errors(response: BaseModel):
        errors = getattr(response, "errors", None)
        if errors and isinstance(errors, list) and all(isinstance(e, ChalkError) for e in errors):
            errors = cast(List[ChalkError], errors)
            raise ChalkBaseException(errors=errors)

    @staticmethod
    def _raise_if_http_error(response: requests.Response):
        if response.status_code < 400:
            return

        def _standardized_raise():
            try:
                standardized_exception = _ChalkHTTPException.parse_obj(response.json())
            except Exception:
                pass
            else:
                raise ChalkBaseException(
                    errors=standardized_exception.errors,
                    trace_id=standardized_exception.trace,
                    detail=standardized_exception.detail,
                )

        def _fallback_raise():
            trace_id = None
            if hasattr(response, "headers") and isinstance(response.headers, Mapping):
                trace_id = response.headers.get(_CHALK_TRACE_ID_KEY)

            detail = None
            try:
                response_json = response.json()
                if isinstance(response_json, Mapping):
                    detail = response_json.get("detail")
            except RequestsJSONDecodeError:
                pass

            status_code = response.status_code
            known_error_code = None
            if status_code == 401:
                known_error_code = ErrorCode.UNAUTHENTICATED
            elif status_code == 403:
                known_error_code = ErrorCode.UNAUTHORIZED

            message = (
                f"{status_code} {detail}" if detail else f"Unexpected Chalk server error with status code {status_code}"
            )
            chalk_error = ChalkError(
                code=known_error_code or ErrorCode.INTERNAL_SERVER_ERROR,
                message=message,
            )
            raise ChalkBaseException(errors=[chalk_error], trace_id=trace_id)

        _standardized_raise()
        _fallback_raise()

    def _request(
        self,
        method: str,
        uri: str,
        response: Optional[Type[T]],
        json: Optional[BaseModel],
        environment_override: Optional[str],
        preview_deployment_id: Optional[str],
        branch: Optional[Union[BranchId, _EMPTY]],
        data: Optional[bytes] = None,
        api_server_override: Optional[str] = None,
        metadata_request: bool = True,
        extra_headers: Optional[dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> T:
        if extra_headers is None:
            extra_headers = {}

        # Track whether we already exchanged credentials for this request
        exchanged_credentials = False
        if not self._exchanged_credentials:
            exchanged_credentials = True
            try:
                self._exchange_credentials()
            except HTTPError as e:
                self._raise_if_http_error(response=e.response)
        headers = self._get_headers(
            environment_override=environment_override,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        headers.update(extra_headers)
        default_api_server = self._config.api_server if metadata_request else self._config.query_server
        url = urljoin(api_server_override or default_api_server, uri)
        json_body = json and json.dict()
        r = self.session.request(method=method, headers=headers, url=url, json=json_body, data=data)
        if r.status_code in (401, 403) and not exchanged_credentials:
            # It is possible that credentials expired, or that we changed permissions since we last
            # got a token. Exchange them and try again
            self._exchange_credentials()
            r = self.session.request(
                method=method, headers=headers, url=url, json=json_body, data=data, timeout=timeout or 60.0
            )

        self._raise_if_http_error(response=r)
        if response is None:
            return r
        return response(**r.json())

    def _load_branches(self):
        try:
            branch = self._config.branch
            result = self._request(
                method="GET",
                uri="/v1/branches",
                response=_BranchMetadataResponse,
                json=None,
                environment_override=None,
                preview_deployment_id=None,
                branch=branch,
                api_server_override=self._get_local_server_override(None),
            )

        except ChalkBaseException as e:
            # If we can't get branches, we can't do anything else
            self._raise_bad_creds_error(errors=e.errors)
        our_branch = next((b for b in result.branches if b.name == branch), None)
        if our_branch is None:
            project_config = load_project_config()
            if project_config:
                project_path = Path(project_config.local_path).parent
            else:
                project_path = "<Your Chalk project directory>"
            branch_names = list(reversed(sorted(result.branches, key=lambda b: str(b.latest_deployment_time))))
            limit = 10
            available_branches = "\n".join(f"  - {b.name}" for b in branch_names[:limit])
            if len(branch_names) > limit:
                available_text = f"The {limit} most recently used branches are:"
            else:
                available_text = "Available branches are:"
            raise ChalkCustomException(
                f"""Your client is set up to use a branch '{branch}' that does not exist. {available_text}

{available_branches}

To deploy new features and resolvers in a Jupyter notebook, you must first create a branch from the Chalk CLI.

>>> cd "{project_path}" && chalk apply --branch "{branch}"

Then, you can run this cell again and see your new work! For more docs on applying changes to branches, see:

https://docs.chalk.ai/cli/apply
"""
            )

    def _raise_bad_creds_error(self, errors: Optional[List[ChalkError]] = None):
        exc = ChalkCustomException(
            f"""We weren't able to authenticate you with the Chalk API. Authentication was attempted with the following credentials:

    Client ID:     {self._config.client_id}
    Client Secret: {'*' * len(self._config.client_secret)}
    Branch:        {self._config.branch or ''}
    Environment:   {self._config.active_environment or ''}
    API Server:    {self._config.api_server}
    chalkpy:       v{chalkpy_version}

If these credentials look incorrect to you, try running

>>> chalk login

from the command line from '{os.getcwd()}'. If you are still having trouble, please contact Chalk support.""",
            errors=errors,
        )
        raise exc

    def whoami(self) -> WhoAmIResponse:
        try:
            return self._request(
                method="GET",
                uri="/v1/who-am-i",
                response=WhoAmIResponse,
                json=None,
                environment_override=None,
                preview_deployment_id=None,
                metadata_request=True,
                branch=None,
            )
        except ChalkBaseException as e:
            self._raise_bad_creds_error(errors=e.errors)

    # TODO can we go ahead and expose this model to clients? Seems useful
    def _get_branch_info(self) -> _BranchMetadataResponse:
        result = self._request(
            method="GET",
            uri="/v1/branches",
            response=_BranchMetadataResponse,
            json=None,
            environment_override=None,
            preview_deployment_id=None,
            branch=_EMPTY,
            api_server_override=self._get_local_server_override(None),
        )
        return result

    def get_branches(self) -> List[str]:
        branches = self._get_branch_info().branches
        return sorted([b.name for b in branches])

    def get_branch(self) -> Optional[str]:
        return self._config.branch

    def set_branch(self, branch_name: Optional[str]):
        if branch_name is not None:
            branches = self._get_branch_info().branches
            if not any(x.name == branch_name for x in branches):
                raise ValueError(
                    f"A branch with the name '{branch_name}' does not exist in this environment. Run ChalkClient.create_branch(branch_name) to create a new branch. "
                    f"To see a list of available branches, use ChalkClient.get_branches()."
                )
        self._config.branch = branch_name

    def upload_features(
        self,
        input: Mapping[FeatureReference, Any],
        branch: Optional[BranchId] = ...,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        return self.query(
            input=input,
            output=list(input.keys()),
            staleness=None,
            environment=environment,
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
            branch=branch,
        ).errors

    def query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference],
        now: Optional[datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        context: Optional[OnlineQueryContext] = None,  # Deprecated.
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
    ) -> OnlineQueryResponseImpl:
        environment = environment or (context and context.environment)
        tags = tags or (context and context.tags)

        all_warnings: List[str] = []
        encoded_inputs, encoding_warnings = recursive_encode_inputs(input)
        all_warnings += encoding_warnings
        outputs, encoding_warnings = encode_outputs(output)
        all_warnings += encoding_warnings

        if branch is Ellipsis:
            branch = self._config.branch

        now_str = None
        if now is not None:
            if now.tzinfo is None:
                now = now.astimezone(tz=timezone.utc)
            now_str = now.isoformat()

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[ensure_feature(k).root_fqn] = v

        request = OnlineQueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            now=now_str,
            staleness=staleness_encoded,
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
            explain=explain,
            include_meta=include_meta or explain,
            store_plan_stages=store_plan_stages,
            encoding_options=encoding_options or FeatureEncodingOptions(),
        )

        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=OnlineQueryResponse,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
            api_server_override=self._get_local_server_override(None),
        )
        return OnlineQueryResponseImpl(data=resp.data, errors=resp.errors or [], warnings=all_warnings, meta=resp.meta)

    def multi_query(
        self,
        queries: list[OnlineQuery],
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
        use_feather: Optional[bool] = True,
        compression: Optional[str] = "uncompressed",
    ) -> BulkOnlineQueryResponse:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is not None:
            # TODO: Support this for branch deployments.
            raise NotImplementedError(
                f"Query-many is not currently supported for branch deployments."
                f" Client is currently connected to the branch '{self._config.branch}'."
            )
        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name
        if use_feather:
            import polars as pl
            import pyarrow
            import pyarrow.feather as feather

            buffer = BytesIO()
            buffer.write(MULTI_QUERY_MAGIC_STR)
            all_warnings: List[str] = []
            for query in queries:
                tags = query.tags
                encoded_inputs = {str(k): v for k, v in query.input.items()}
                outputs, encoding_warnings = encode_outputs(query.output)
                all_warnings += encoding_warnings
                request = OnlineQueryManyRequest(
                    inputs=encoded_inputs,
                    outputs=outputs,
                    staleness={}
                    if query.staleness is None
                    else {ensure_feature(k).root_fqn: v for k, v in query.staleness.items()},
                    context=OnlineQueryContext(
                        environment=environment,
                        tags=tags,
                    ),
                    deployment_id=preview_deployment_id,
                    branch_id=branch,
                    correlation_id=correlation_id,
                    query_name=query_name,
                    meta=meta,
                )

                _write_query_to_buffer(buffer, request, compression=compression)

            buffer.seek(0)
            resp = self._request(
                method="POST",
                uri="/v1/query/feather",
                data=buffer.getvalue(),
                json=None,
                response=None,
                environment_override=environment,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                metadata_request=False,
                extra_headers=extra_headers,
            )

            if resp.headers.get("Content-Type") == "application/octet-stream":
                all_responses = OnlineQueryResponseFeather.deserialize(resp.content)

                bulk_results = []
                for query_name, serialized_single_result in all_responses.query_results_bytes.items():
                    single_feather_result = OnlineQueryResultFeather.deserialize(serialized_single_result)
                    scalars_df = None
                    groups_dfs = None
                    meta = QueryMeta(**json.loads(single_feather_result.meta)) if single_feather_result.meta else None
                    errors = (
                        [ChalkError(**json.loads(error_json_str)) for error_json_str in single_feather_result.errors]
                        if single_feather_result.errors
                        else None
                    )
                    if single_feather_result.has_data:
                        scalars_pa = pyarrow.feather.read_table(BytesIO(single_feather_result.scalar_data))
                        scalars_pl = pl.from_arrow(scalars_pa)
                        scalars_df = scalars_pl

                        groups_dfs = {}
                        for feature_name, feature_results_bytes in single_feather_result.groups_data.items():
                            feature_pa = pyarrow.feather.read_table(BytesIO(feature_results_bytes))
                            feature_pl = pl.from_arrow(feature_pa)
                            groups_dfs[feature_name] = feature_pl

                    bulk_result = BulkOnlineQueryResult(
                        scalars_df=scalars_df, groups_dfs=groups_dfs, errors=errors, meta=meta
                    )
                    bulk_results.append(bulk_result)
                return BulkOnlineQueryResponse(results=bulk_results)
            else:
                raise ChalkBaseException(
                    errors=None, detail="Unexpected response from server -- failed to receive Feather encoded data."
                )

    def query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], Any],
        output: Sequence[FeatureReference],
        now: Optional[Sequence[datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        context: Optional[OnlineQueryContext] = None,  # Deprecated.
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> BulkOnlineQueryResponse:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is not None:
            # TODO: Support this for branch deployments.
            raise NotImplementedError(
                f"Query-many is not currently supported for branch deployments."
                f" Client is currently connected to the branch '{self._config.branch}'."
            )

        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name

        now_str = None
        if now is not None:
            now_str = []
            for ts in now:
                if ts.tzinfo is None:
                    ts = ts.astimezone(tz=timezone.utc)
                now_str.append(ts.isoformat())

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[ensure_feature(k).root_fqn] = v

        environment = environment or (context and context.environment)
        tags = tags or (context and context.tags)
        # TODO: We're doing a lame encoding here b/c recursive_encode will treat our lists
        #       as json to serialize.
        # encoded_inputs, encoding_warnings = recursive_encode(input)
        encoded_inputs = {str(k): v for k, v in input.items()}
        outputs, encoding_warnings = encode_outputs(output)
        request = OnlineQueryManyRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            now=now_str,
            staleness=staleness_encoded,
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
            # explain=explain,
        )

        buffer = BytesIO()

        buffer.write(MULTI_QUERY_MAGIC_STR)
        _write_query_to_buffer(buffer, request, compression="uncompressed")

        buffer.seek(0)

        resp = self._request(
            method="POST",
            uri="/v1/query/feather",
            data=buffer.getvalue(),
            json=None,
            response=None,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
        )

        import polars as pl
        import pyarrow
        import pyarrow.feather as feather

        assert (
            resp.headers.get("Content-Type") == "application/octet-stream"
        ), "The response wasn't in the expected byte format!"
        all_responses = OnlineQueryResponseFeather.deserialize(resp.content)

        bulk_results = []
        for query_name, serialized_single_result in all_responses.query_results_bytes.items():
            single_feather_result = OnlineQueryResultFeather.deserialize(serialized_single_result)
            scalars_df = None
            groups_dfs = None
            meta = QueryMeta(**json.loads(single_feather_result.meta)) if single_feather_result.meta else None
            errors = (
                [ChalkError(**json.loads(error_json_str)) for error_json_str in single_feather_result.errors]
                if single_feather_result.errors
                else None
            )
            if single_feather_result.has_data:
                scalars_pa = pyarrow.feather.read_table(BytesIO(single_feather_result.scalar_data))
                scalars_pl = pl.from_arrow(scalars_pa)
                scalars_df = scalars_pl

                groups_dfs = {}
                for feature_name, feature_results_bytes in single_feather_result.groups_data.items():
                    feature_pa = pyarrow.feather.read_table(BytesIO(feature_results_bytes))
                    feature_pl = pl.from_arrow(feature_pa)
                    groups_dfs[feature_name] = feature_pl

            bulk_result = BulkOnlineQueryResult(scalars_df=scalars_df, groups_dfs=groups_dfs, errors=errors, meta=meta)
            bulk_results.append(bulk_result)
        return BulkOnlineQueryResponse(results=bulk_results)

    def query_many(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], Any],
        output: Sequence[FeatureReference],
        now: Optional[Sequence[datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        context: Optional[OnlineQueryContext] = None,  # Deprecated.
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
        use_feather: Optional[bool] = True,
    ) -> OnlineQueryResponseImpl:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is not None:
            # TODO: Support this for branch deployments.
            raise NotImplementedError(
                f"Query-many is not currently supported for branch deployments."
                f" Client is currently connected to the branch '{self._config.branch}'."
            )

        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name

        now_str = None
        if now is not None:
            now_str = []
            for ts in now:
                if ts.tzinfo is None:
                    ts = ts.astimezone(tz=timezone.utc)
                now_str.append(ts.isoformat())

        environment = environment or (context and context.environment)
        tags = tags or (context and context.tags)
        # TODO: We're doing a lame encoding here b/c recursive_encode will treat our lists
        #       as json to serialize.
        # encoded_inputs, encoding_warnings = recursive_encode(input)
        encoded_inputs = {str(k): v for k, v in input.items()}
        outputs, encoding_warnings = encode_outputs(output)
        request = OnlineQueryManyRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            now=now_str,
            staleness={} if staleness is None else {ensure_feature(k).root_fqn: v for k, v in staleness.items()},
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
            # explain=explain,
        )

        if use_feather:
            import pyarrow
            import pyarrow.feather as feather

            buffer = BytesIO()

            buffer.write(MULTI_QUERY_MAGIC_STR)
            _write_query_to_buffer(buffer, request, compression="uncompressed")

            buffer.seek(0)

            resp = self._request(
                method="POST",
                uri="/v1/query/feather",
                data=buffer.getvalue(),
                json=None,
                response=None,
                environment_override=environment,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                metadata_request=False,
                extra_headers=extra_headers,
            )

            if resp.headers.get("Content-Type") == "application/octet-stream":
                # TODO: This returns a pyarrow table, which does NOT
                #  match the type signature.
                return _decode_multi_query_responses(resp.content)[0]
            else:
                resp = OnlineQueryResponse(**resp.json())
        else:
            branch = branch or self._config.branch

            resp = self._request(
                method="POST",
                uri="/v1/query_many/online/detailed",
                json=request,
                response=OnlineQueryResponse,
                environment_override=environment,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                extra_headers=extra_headers,
            )
        return OnlineQueryResponseImpl(
            data=resp.data,
            errors=resp.errors or [],
            warnings=encoding_warnings,
        )

    def offline_query(
        self,
        input: Optional[Union[Mapping[FeatureReference, Any], pd.DataFrame, pl.DataFrame, DataFrame]] = None,
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        environment: Optional[EnvironmentId] = None,
        dataset_name: Optional[str] = None,
        branch: Optional[BranchId] = ...,  # distinguished from user explicitly specifying branch=None
        correlation_id: str | None = None,
        max_samples: Optional[int] = None,
        wait: bool = False,
        show_progress: bool = True,
        recompute_features: Union[bool, List[FeatureReference]] = False,
        lower_bound: Optional[datetime] = None,
        upper_bound: Optional[datetime] = None,
        store_plan_stages: bool = False,
        explain: Union[bool, Literal["only"]] = False,
        tags: Optional[List[str]] = None,
    ) -> DatasetImpl:
        if branch is Ellipsis:
            branch = self._config.branch
        unbranched = branch is None

        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        del pl  # unused

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if input is None:
            query_input = None
        else:
            query_input = _to_offline_query_input(input, input_times)

        response = self._create_dataset_job(
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            query_input=query_input,
            dataset_name=dataset_name,
            branch=branch,
            correlation_id=correlation_id,
            context=OfflineQueryContext(environment=environment),
            max_samples=max_samples,
            recompute_features=recompute_features,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            store_plan_stages=store_plan_stages,
            tags=tags,
        )

        initialized_dataset = dataset_from_response(response, self)

        revision = initialized_dataset.revisions[-1]
        revision._show_progress = show_progress
        # Set as hydrated so that we never call hydration on datasets from unbranched queries.
        revision._hydrated = revision._hydrated or unbranched or (isinstance(wait, float) and wait == 0.0)

        if not wait:
            return initialized_dataset

        revision.wait_for_completion()
        initialized_dataset.is_finished = True
        return initialized_dataset

    def sample(
        self,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        output_id: bool = False,
        output_ts: bool = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[BranchId] = None,
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        context = OfflineQueryContext(environment=environment)
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        response = self._create_and_await_offline_query_job(
            query_input=None,
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            max_samples=max_samples,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            preview_deployment_id=None,
            lazy=False,
            tags=tags,
        )
        if isinstance(response, pl.LazyFrame):
            response = response.collect()

        return response.to_pandas()

    def get_dataset(
        self,
        dataset_name: str,
        environment: Optional[EnvironmentId] = None,
    ) -> DatasetImpl:
        response: DatasetResponse = self._get_dataset(
            dataset_name=dataset_name,
            environment=environment,
        )
        if response.errors:
            raise ChalkCustomException(
                message=f"Failed to download dataset `{dataset_name}`",
                errors=response.errors,
            )
        return dataset_from_response(response, self)

    def delete_features(
        self,
        namespace: str,
        features: Optional[List[str]],
        tags: Optional[List[str]],
        primary_keys: List[str],
        environment: Optional[EnvironmentId] = None,
    ) -> FeatureObservationDeletionResponse:
        if self._config.branch is not None:
            raise NotImplementedError(
                f"Feature deletion is not currently supported for branch deployments. Client is currently connected to the branch '{self._config.branch}'."
            )
        _logger.debug(
            (
                f"Performing deletion in environment {environment if environment else 'default'} and namespace "
                f"{namespace} with targets that match the following criteria: features={features}, tags={tags}, "
                f"and primary_keys={primary_keys}"
            )
        )

        return self._request(
            method="DELETE",
            uri="/v1/features/rows",
            json=FeatureObservationDeletionRequest(
                namespace=namespace,
                features=features,
                tags=tags,
                primary_keys=primary_keys,
            ),
            response=FeatureObservationDeletionResponse,
            environment_override=environment,
            preview_deployment_id=None,
            branch=None,
        )

    def drop_features(
        self,
        namespace: str,
        features: List[str],
        environment: Optional[EnvironmentId] = None,
    ) -> FeatureDropResponse:
        if self._config.branch is not None:
            raise NotImplementedError(
                f"Feature dropping is not currently supported for branch deployments. Client is currently connected to the branch '{self._config.branch}'."
            )
        _logger.debug(
            (
                f"Performing feature drop in environment {environment if environment else 'default'} and namespace "
                f"{namespace} for the following features:{features}."
            )
        )
        return self._request(
            method="DELETE",
            uri="/v1/features/columns",
            json=FeatureDropRequest(namespace=namespace, features=features),
            response=FeatureDropResponse,
            environment_override=environment,
            preview_deployment_id=None,
            branch=None,
        )

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
    ) -> ResolverRunResponse:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is not None:
            raise NotImplementedError(
                f"Triggering resolver runs is not currently supported for branch deployments."
                f"Client is currently connected to the branch '{self._config.branch}'."
            )
        _logger.debug(f"Triggering resolver {resolver_fqn} to run")
        return self._request(
            method="POST",
            uri="/v1/runs/trigger",
            json=TriggerResolverRunRequest(resolver_fqn=resolver_fqn),
            response=ResolverRunResponse,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

    def get_run_status(
        self,
        run_id: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = ...,
    ) -> ResolverRunResponse:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is not None:
            raise NotImplementedError(
                f"Triggering resolver runs is not currently supported for branch deployments."
                f"Client is currently connected to the branch '{self._config.branch}'."
            )
        response = self._request(
            method="GET",
            uri=f"/v1/runs/{run_id}",
            response=ResolverRunResponse,
            json=None,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

        return response

    def _create_and_await_offline_query_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[BranchId],
        context: OfflineQueryContext,
        output_id: bool,
        output_ts: bool,
        preview_deployment_id: Optional[str],
        lazy: bool = True,
        tags: Optional[List[str]] = None,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            recompute_features=True,
            tags=tags,
        )
        response = self._create_offline_query_job(
            request=req,
            context=context,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response)
        return self._await_offline_query_job(
            job_id=response.job_id,
            outputs=[*optional_output, *required_output],
            lazy=lazy,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
        )

    @overload
    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: Literal[False] = ...,
        branch: Optional[BranchId] = ...,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        ...

    @overload
    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: Literal[True],
        branch: Optional[BranchId] = ...,
    ) -> List[str]:
        ...

    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: bool = False,
        branch: Optional[BranchId] = None,
    ) -> Union[pl.DataFrame, pl.LazyFrame, List[str]]:
        while True:
            status = self._get_job_status(job_id=job_id, environment=context and context.environment, branch=branch)
            if status.is_finished:
                break
            time.sleep(0.5)
        if urls_only:
            return status.urls
        return load_dataset(
            uris=status.urls,
            output_features=outputs,
            version=DatasetVersion(status.version),
            output_id=output_id,
            output_ts=output_ts,
            columns=status.columns,
            lazy=lazy,
        )

    def _await_offline_query_input(
        self,
        job_id: uuid.UUID,
        lazy: bool,
        context: Optional[OfflineQueryContext],
        urls_only: bool = False,
        branch: Optional[BranchId] = None,
    ) -> Union[pl.DataFrame, pl.LazyFrame, List[str]]:
        status = self._get_query_inputs(job_id=job_id, environment=context and context.environment, branch=branch)
        if urls_only:
            return status.urls
        return load_dataset(
            uris=status.urls,
            output_features=None,
            version=DatasetVersion(status.version),
            columns=status.columns,
            lazy=lazy,
        )

    def _recompute_dataset(
        self,
        dataset_name: Optional[str],
        dataset_id: Optional[uuid.UUID],
        revision_id: Optional[uuid.UUID],
        features: List[Union[str, Any]],
        branch: BranchId,
        environment: Optional[EnvironmentId],
    ) -> DatasetRecomputeResponse:
        request = DatasetRecomputeRequest(
            dataset_name=dataset_name,
            dataset_id=str(dataset_id) if dataset_id is not None else None,
            revision_id=str(revision_id) if revision_id is not None else None,
            features=[str(f) for f in features],
            branch=branch,
        )
        return self._request(
            method="POST",
            uri="/v4/dataset/recompute",
            json=request,
            response=DatasetRecomputeResponse,
            environment_override=environment,
            preview_deployment_id=None,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
        )

    def _create_dataset_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[BranchId],
        context: OfflineQueryContext,
        correlation_id: Optional[str] = None,
        recompute_features: Union[bool, List[FeatureReference]] = False,
        lower_bound: Optional[datetime] = None,
        upper_bound: Optional[datetime] = None,
        store_plan_stages: bool = False,
        explain: Union[bool, Literal["only"]] = False,
        tags: Optional[List[str]] = None,
    ) -> DatasetResponse:
        if isinstance(recompute_features, list):
            recompute_features = [
                unwrap_feature(f).fqn if isinstance(f, FeatureWrapper) else f for f in recompute_features
            ]
        if lower_bound and lower_bound.tzinfo is None:
            lower_bound = lower_bound.astimezone()
        if upper_bound and upper_bound.tzinfo is None:
            upper_bound = upper_bound.astimezone()
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            recompute_features=recompute_features,
            observed_at_lower_bound=lower_bound and lower_bound.isoformat(),
            observed_at_upper_bound=upper_bound and upper_bound.isoformat(),
            store_plan_stages=store_plan_stages,
            correlation_id=correlation_id,
            explain=explain,
            tags=tags,
        )
        response = self._create_dataset_request(
            request=req,
            context=context,
            preview_deployment_id=None,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response)
        return response

    def compute_resolver_output(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        resolver: str,
        context: Optional[OfflineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> pl.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if context is None:
            context = OfflineQueryContext()
        query_input = _to_offline_query_input(input, input_times)
        request = ComputeResolverOutputRequest(input=query_input, resolver_fqn=resolver)
        response = self._request(
            method="POST",
            uri="/v1/compute_resolver_output",
            json=request,
            response=ComputeResolverOutputResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response)

        while True:
            status = self._get_compute_job_status(
                job_id=response.job_id,
                context=context,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
            )
            if status.is_finished:
                break
            time.sleep(0.5)

        df = load_dataset(
            uris=status.urls,
            version=status.version,
            executor=None,
            columns=status.columns,
        )
        if isinstance(df, pl.LazyFrame):
            df = df.collect()
        return df

    def create_branch(
        self,
        branch_name: str,
        create_only: bool = True,
        source_deployment_id: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
    ) -> BranchDeployResponse:
        available_branches = self.get_branches()
        if branch_name in available_branches and create_only:
            raise RuntimeError(
                f"The branch `{branch_name}` already exists."
                f" To connect your client to an existing branch, specify the 'branch' parameter when "
                f"creating a ChalkClient. Available branches are: {available_branches}"
            )

        request = BranchDeployRequest(
            branch_name=branch_name,
            create_only=create_only,
            source_deployment_id=source_deployment_id,
        )
        try:
            resp = self._request(
                method="POST",
                uri=f"/v1/branches/{branch_name}/source",
                response=BranchDeployResponse,
                json=request,
                branch=_EMPTY,
                environment_override=environment,
                preview_deployment_id=None,
            )
        except ChalkBaseException as e:
            raise ChalkCustomException.from_base(e, f"Failed to deploy branch `{branch_name}`.")

        if notebook.is_notebook():
            self._display_branch_creation_response(resp)
            self._display_button_to_change_branch(branch_name)
        return resp

    def _display_branch_creation_response(self, resp: BranchDeployResponse):
        from IPython.display import display_markdown

        if resp.new_branch_created:
            prefix = "Created new "
        else:
            prefix = "Deployed "
        text = f"{prefix} branch `{resp.branch_name}` with source from deployment `{resp.source_deployment_id}`."
        display_markdown(text, raw=True)

    def _display_button_to_change_branch(self, branch_name: str):
        if not notebook.is_notebook():
            return
        try:
            from IPython.core.display_functions import display
            from ipywidgets import interactive, widgets

            layout = widgets.Layout(width="auto")
            button0 = widgets.Button(
                description=f"Set current branch to '{branch_name}'",
                tooltip=f'Equivalent to client.set_branch("{branch_name}")',
                layout=layout,
            )
            output0 = widgets.Output()
            display(button0, output0)

            def on_button_clicked0(_):
                with output0:
                    old_branch = self._config.branch
                    self._config.branch = branch_name
                    old_branch_text = ""
                    if old_branch is not None:
                        old_branch_text = f" from `{old_branch}`"
                    from IPython.display import display_markdown

                    display_markdown(f"Set branch for Chalk client{old_branch_text} to `{branch_name}`.", raw=True)

            button0.on_click(on_button_clicked0)
        except Exception:
            pass

    def _get_compute_job_status(
        self,
        job_id: str,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v1/compute_resolver_output/{job_id}",
            response=GetOfflineQueryJobResponse,
            json=None,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

    def _create_dataset_request(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ) -> DatasetResponse:
        response = self._request(
            method="POST",
            uri="/v4/offline_query",
            json=request,
            response=DatasetResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
        )
        return response

    def _create_offline_query_job(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ):
        response = self._request(
            method="POST",
            uri="/v2/offline_query",
            json=request,
            response=CreateOfflineQueryJobResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        return response

    def _get_job_status(
        self, job_id: uuid.UUID, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/offline_query/{job_id}",
            response=GetOfflineQueryJobResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
        )

    def _get_query_inputs(
        self, job_id: uuid.UUID, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/offline_query_inputs/{job_id}",
            response=GetOfflineQueryJobResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
        )

    def _get_dataset(self, dataset_name: str, environment: Optional[EnvironmentId]) -> DatasetResponse:
        return self._request(
            method="GET",
            uri=f"/v3/offline_query/{dataset_name}",
            response=DatasetResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=None,
        )

    def _get_anonymous_dataset(
        self, revision_id: str, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> DatasetImpl:
        try:
            response = self._request(
                method="GET",
                uri=f"/v4/offline_query/{revision_id}",
                response=DatasetResponse,
                environment_override=environment,
                json=None,
                preview_deployment_id=None,
                branch=branch,
                api_server_override=self._get_local_server_override(branch),
            )
        except ChalkBaseException as e:
            raise ChalkCustomException.from_base(
                e,
                message=f"Failed to get dataset for revision id '{revision_id}'.",
            )

        return dataset_from_response(response, self)

    def _get_batch_report(self, operation_id: uuid.UUID, environment_id: EnvironmentId) -> Optional[BatchReport]:
        try:
            response = self._request(
                method="GET",
                uri=f"/v4/offline_query/{operation_id}/status",
                response=BatchReportResponse,
                json=None,
                environment_override=environment_id,
                preview_deployment_id=None,
                branch=_EMPTY,
            )
        except Exception:
            return None

        return response.report

    def _send_updated_entity(
        self, environment: Optional[EnvironmentId], pickled_entity: bytes
    ) -> UpdateGraphEntityResponse:
        resp = self._request(
            method="POST",
            uri="/v1/update_graph_entity",
            response=UpdateGraphEntityResponse,
            json=None,
            data=pickled_entity,
            environment_override=environment,
            preview_deployment_id=None,
            branch=None,
            api_server_override=self._get_local_server_override(None),
        )
        if resp.errors:
            raise ChalkBaseException(errors=resp.errors)
        return resp

    def _await_operation_completion(
        self,
        operation_id: uuid.UUID,
        environment_id: EnvironmentId,
        show_progress: bool = True,
        caller_method: Optional[str] = None,
    ):
        ProgressService(
            operation_id=operation_id,
            client=self,
            caller_method=caller_method,
            environment_id=environment_id,
        ).await_operation(show_progress=show_progress)

    def _get_local_server_override(self, body_branch: Optional[BranchId]) -> Optional[str]:
        branched = body_branch is not None or self._config.branch is not None
        server = self._config.api_server
        is_local = server.startswith("http://localhost") or server.startswith("http://127.0.0.1")

        server_override = None
        if branched and is_local:
            server_override = "http://localhost:1337"

        return server_override

    def _get_upsert_graph_gql_from_branch(
        self,
        branch: Union[BranchId, Ellipsis] = ...,
        environment: Optional[EnvironmentId] = None,
    ) -> dict:
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is None:
            raise RuntimeError("No branch specified or set in client. This method only works for branch deployments.")
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                f"The branch `{branch}` does not exist. "
                f"Available branches are: {available_branches}. "
                f"To create a branch, use `ChalkClient.create_branch(...)`"
            )
        result = self._request(
            method="GET",
            uri=f"/v1/branch/{branch}/graph_gql",
            environment_override=environment,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
            response=None,  # get the JSON
            preview_deployment_id=None,
            json=None,
        )
        return result.json()

    def reset_branch(self, branch: BranchIdParam = ..., environment: Optional[EnvironmentId] = None):
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is None:
            raise RuntimeError("No branch specified or set in client. This method only works for branch deployments.")
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                f"The branch `{branch}` does not exist. "
                f"Available branches are: {available_branches}. "
                f"To create a branch, use `ChalkClient.create_branch(...)`"
            )
        self._request(
            method="POST",
            uri=f"/v1/branch/{branch}/reset",
            environment_override=environment,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
            response=None,
            preview_deployment_id=None,
            json=None,
        )

    def branch_state(
        self,
        branch: Union[BranchId, Ellipsis] = ...,
        environment: Optional[EnvironmentId] = None,
    ):
        if branch is Ellipsis:
            branch = self._config.branch
        if branch is None:
            raise RuntimeError("No branch specified or set in client. This method only works for branch deployments.")
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                f"The branch `{branch}` does not exist. "
                f"Available branches are: {available_branches}. "
                f"To create a branch, use `ChalkClient.create_branch(...)`"
            )
        result = self._request(
            method="GET",
            uri=f"/v1/branch/{branch}/graph_state",
            environment_override=environment,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
            response=None,  # get the JSON
            preview_deployment_id=None,
            json=None,
        )
        return BranchGraphSummary.from_dict(result.json())

    def test_streaming_resolver(
        self,
        resolver: Union[str, Resolver],
        num_messages: Optional[int] = None,
        message_filepath: Optional[str] = None,
        message_keys: Optional[List[str]] = None,
        message_bodies: Optional[List[Union[str, bytes]]] = None,
        message_timestamps: Optional[List[Union[str, datetime]]] = None,
        branch: Union[BranchId, Ellipsis] = ...,
        environment: Optional[EnvironmentId] = None,
    ) -> StreamResolverTestResponse:
        resolver_fqn = resolver.fqn if isinstance(resolver, Resolver) else resolver
        if branch is Ellipsis:
            branch = self._config.branch

        if num_messages is None and message_filepath is None and (message_keys is None or message_bodies is None):
            raise ValueError(
                "One of 'num_messages', 'test_message_filepath' or ('test_message_keys' and 'test_message_bodies')"
                " must be provided."
            )
        payloads = (
            self._validate_test_stream_resolver_inputs(
                message_filepath=message_filepath,
                message_keys=message_keys,
                message_bodies=message_bodies,
                message_timestamps=message_timestamps,
            )
            if message_keys is not None or message_filepath is not None
            else None
        )
        request = StreamResolverTestRequest(
            resolver_fqn=resolver_fqn, num_messages=num_messages, test_messages=payloads
        )
        result = self._request(
            method="POST",
            uri=f"/v1/test_stream_resolver/",
            environment_override=environment,
            json=request,
            branch=branch,
            api_server_override=self._get_local_server_override(branch),
            response=StreamResolverTestResponse,
            preview_deployment_id=None,
        )
        return result

    def _validate_test_stream_resolver_inputs(
        self,
        message_filepath: Optional[str] = None,
        message_keys: Optional[List[str]] = None,
        message_bodies: Optional[List[Union[str, bytes]]] = None,
        message_timestamps: Optional[List[Union[str, datetime]]] = None,
    ) -> List[StreamResolverTestMessagePayload]:
        if message_filepath and (message_keys or message_bodies):
            raise ValueError("Only one of 'message_filepath' or ('message_keys' and 'message_bodies') can be provided.")
        if sum([message_keys is None, message_bodies is None]) == 1:
            raise ValueError("Both of 'message_keys' and 'message_bodies' must be provided")
        if message_filepath:
            message_keys = []
            message_bodies = []
            message_timestamps = []
            with open(message_filepath) as file:
                for i, line in enumerate(file):
                    try:
                        json_message = json.loads(line.rstrip())
                        if "message_key" not in json_message:
                            raise ValueError(f"Key 'message_key' missing from line {i + 1}")
                        if "message_body" not in json_message:
                            raise ValueError(f"Key 'message_body' missing from line {i + 1}")
                        message_keys.append(json_message["message_key"])
                        message_bodies.append(json.dumps(json_message["message_body"]))
                        if "message_timestamp" in json_message:
                            timestamp_string = json_message["message_timestamp"]
                            message_timestamps.append(timestamp_string)
                    except Exception as e:
                        raise ValueError(f"Could not parse line {line} from file {message_filepath}: error {e}")

        if len(message_keys) != len(message_bodies) or len(message_keys) == 0:
            raise ValueError(
                f"The length of 'message_keys' and the length of 'message_bodies' must be equal and nonzero. "
                f"{len(message_keys)} != {len(message_bodies)}"
            )
        if message_timestamps and len(message_keys) != len(message_timestamps):
            raise ValueError(
                f"The length of 'message_keys' and the length of 'message_timestamps' must be equal and nonzero. "
                f"{len(message_keys)} != {len(message_bodies)}"
            )
        if message_timestamps:
            timestamp_datetimes = []
            for timestamp in message_timestamps:
                try:
                    if isinstance(timestamp, str):
                        timestamp = parser.parse(timestamp)
                    if timestamp.tzinfo is None:
                        raise ValueError(f"timestamp {timestamp} must be timezone aware")
                    timestamp_datetimes.append(timestamp)
                except Exception as e:
                    raise ValueError(f"Could not parse timestamp {timestamp}, {e}")
        else:
            timestamp_datetimes = None
        bodies_are_bytes = True if isinstance(message_bodies[0], bytes) else False
        if bodies_are_bytes:
            message_bodies = [base64.b64encode(message).decode("utf-8") for message in message_bodies]
        payloads: List[StreamResolverTestMessagePayload] = [
            StreamResolverTestMessagePayload(
                key=message_keys[i],
                message_str=message_bodies[i] if not bodies_are_bytes else None,
                message_bytes=message_bodies[i] if bodies_are_bytes else None,
                timestamp=timestamp_datetimes[i] if timestamp_datetimes is not None else None,
            )
            for i in range(len(message_keys))
        ]
        return payloads
