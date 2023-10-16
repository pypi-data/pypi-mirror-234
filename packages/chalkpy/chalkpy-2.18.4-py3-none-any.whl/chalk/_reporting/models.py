import collections.abc
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Iterable, List, Optional, Union

from pydantic import BaseModel
from typing_extensions import Self

from chalk.client import ChalkError


class BatchProgress(BaseModel):
    total: int
    computed: int
    failed: int
    start: datetime
    end: Optional[datetime]
    total_duration_s: float

    @classmethod
    def empty(cls) -> "BatchProgress":
        return BatchProgress(
            start=None,
            end=None,
            total=0,
            computed=0,
            failed=0,
            total_duration_s=0.0,
        )

    def __add__(self, other) -> Self:
        if not isinstance(other, BatchProgress):
            raise NotImplementedError(
                f"Can only add ProgressReport to ProgressReport. Received '{type(other).__name__}'"
            )

        return BatchProgress(
            total=self.total + other.total,
            computed=self.computed + other.computed,
            failed=self.failed + other.failed,
            start=min(self.start, other.start),
            total_duration_s=self.total_duration_s + other.total_duration_s,
            end=None,
        )


class BatchProgressSum(BaseModel):
    total: int = 0
    computed: int = 0
    failed: int = 0
    total_duration_s: float = 0.0

    @classmethod
    def from_progresses(cls, *args: Union[BatchProgress, Iterable[BatchProgress]]) -> "BatchProgressSum":
        summed = BatchProgressSum()
        for arg in args:
            if isinstance(arg, collections.abc.Iterable):
                for a in arg:
                    summed += a
            else:
                summed += arg

        return summed

    def __add__(self, other: BatchProgress) -> Self:
        if not isinstance(other, BatchProgress):
            raise NotImplementedError(f"Can only add BatchProgress to BatchProgress. Received '{type(other).__name__}'")

        return BatchProgressSum(
            total=self.total + other.total,
            computed=self.computed + other.computed,
            failed=self.failed + other.failed,
            total_duration_s=self.total_duration_s + other.total_duration_s,
        )


class BatchOpKind(str, Enum):
    OFFLINE_QUERY = "OFFLINE_QUERY"
    RECOMPUTE = "RECOMPUTE"
    CRON = "CRON"


class BatchOpStatus(str, Enum):
    INIT = "INIT"
    COMPUTE_STARTED = "COMPUTE_STARTED"
    COMPUTE_ENDED = "COMPUTE_ENDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ChunkReport(BaseModel):
    # doesn't have its own status.
    # resolver encapsulates the
    # status of the chunk.
    progress: BatchProgress
    generated_at: datetime


class BatchResolverReport(BaseModel):
    resolver_fqn: str
    status: BatchOpStatus
    chunks: List[ChunkReport]
    progress: BatchProgress
    generated_at: datetime
    error: Optional[ChalkError]
    all_errors: Optional[List[ChalkError]] = None


class BatchReport(BaseModel):
    operation_id: str
    operation_kind: BatchOpKind
    status: BatchOpStatus
    resolvers: List[BatchResolverReport]
    progress: BatchProgress
    environment_id: str
    team_id: str
    deployment_id: str
    error: Optional[ChalkError]
    generated_at: datetime
    all_errors: Optional[List[ChalkError]] = None
    operation_metadata: Optional[Dict[str, str]] = None


class BatchReportResponse(BaseModel):
    report: BatchReport
    error: Optional[ChalkError] = None


class InitiateOfflineQueryResponse(BaseModel):
    revision_id: uuid.UUID
