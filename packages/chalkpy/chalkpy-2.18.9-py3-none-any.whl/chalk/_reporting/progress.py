import collections
import time
import uuid
from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict, Iterable, List, Mapping, Optional, Tuple, cast

from rich import box, get_console
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TaskID, TextColumn, TimeElapsedColumn
from rich.style import Style
from rich.table import Table
from rich.text import Text

from chalk import EnvironmentId
from chalk._reporting.models import BatchOpKind, BatchOpStatus, BatchReport
from chalk._reporting.rich.color import PASTELY_CYAN, SHADOWY_LAVENDER, UNDERLYING_CYAN
from chalk._reporting.rich.live import ChalkLive
from chalk.client import ChalkBaseException, ChalkError
from chalk.client.exc import _CHALK_TRACE_ID_KEY
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)

_kind_to_display_type = {
    BatchOpKind.RECOMPUTE: "Dataset Recomputation",
    BatchOpKind.OFFLINE_QUERY: "Offline Query",
}

_MAX_ERRORS_TO_DISPLAY = 10
_TTableRow = Tuple[str, str]


class ProgressService:
    def __init__(
        self,
        operation_id: uuid.UUID,
        client: "ChalkAPIClientImpl",
        environment_id: EnvironmentId,
        caller_method: Optional[str] = None,
    ):
        """
        :param operation_id: The ID of the operation that the ProgressService
            is polling for. This is commonly a `DatasetRevision` ID.
        :param client: A ChalkClient instance
        :param caller_method: Passed only if the caller is a Dataset method. When we call Dataset methods,
            the ProgressService is implicitly called, so we want to explain to the user that their method
            will be executed once the ProgressService finishes polling for the operation to complete.
        """
        self.operation_id = operation_id
        self.client = client
        self.caller_method = f"`{caller_method}()`" if caller_method else None
        self._environment_id = environment_id
        self._operation_kind: Optional[BatchOpKind] = None

    @cached_property
    def resolver_progress(self) -> Progress:
        return Progress(
            TextColumn("  "),
            TimeElapsedColumn(),
            BarColumn(
                finished_style=Style(color=PASTELY_CYAN),
                style=Style(color=SHADOWY_LAVENDER),
                complete_style=Style(color=UNDERLYING_CYAN),
            ),
            MofNCompleteColumn(),
            TextColumn("runs", style=Style(color=PASTELY_CYAN)),
            TextColumn("{task.description}"),
        )

    @cached_property
    def main_progress(self) -> Progress:
        return Progress(
            TextColumn("{task.description}"),
            SpinnerColumn(style=Style(color=SHADOWY_LAVENDER)),
            TimeElapsedColumn(),
        )

    @cached_property
    def explainer_text(self) -> Text:
        explainer_text = Text(
            f"The `DatasetRevision` is still being computed. {self.caller_method} will execute once computation is complete.",
            style=Style(color=PASTELY_CYAN),
        )
        return explainer_text

    @cached_property
    def enclosure_panel(self) -> Panel:
        progress_bar_group = Group(self.main_progress, self.resolver_progress)

        panel_content_table = Table.grid()
        if self.caller_method is not None:
            panel_content_table.add_row(Padding(self.explainer_text, (0, 0, 1, 0)))
        panel_content_table.add_row(progress_bar_group)

        enclosure_panel = Panel.fit(
            panel_content_table, title="chalk", border_style=Style(color=PASTELY_CYAN), box=box.ROUNDED, padding=(1, 2)
        )

        return enclosure_panel

    def handle_resolver_update(self, batch_report: BatchReport, fqn_to_task_id: Dict) -> None:
        for resolver_report in batch_report.resolvers:
            fqn = resolver_report.resolver_fqn
            if fqn not in fqn_to_task_id:
                short_name = fqn.split(".")[-1]
                fqn_to_task_id[fqn] = self.resolver_progress.add_task(
                    description=f"[ {short_name} ]",
                    total=resolver_report.progress.total,
                )

        for resolver_report in batch_report.resolvers:
            fqn = resolver_report.resolver_fqn
            resolver_task_id = fqn_to_task_id[fqn]

            rows_done_new = resolver_report.progress.computed + resolver_report.progress.failed
            self.resolver_progress.update(resolver_task_id, completed=rows_done_new)

    def handle_success(self, main_task_id: TaskID, operation_display_type: str) -> None:
        self.enclosure_panel.title = "chalk ■"
        self.main_progress.update(main_task_id, description=f"{operation_display_type} completed", completed=1)

    def _get_failing_resolver(self, batch_report: BatchReport) -> Optional[str]:
        """
        :return: The name of the resolver that failed, or None if no resolver failed.
        """
        for resolver in batch_report.resolvers:
            if resolver.status == BatchOpStatus.FAILED:
                return resolver.resolver_fqn

    @staticmethod
    def _get_pkey_display_value(error: ChalkError) -> Optional[str]:
        if error.display_primary_key is None:
            return None

        value = ""
        if error.display_primary_key_fqn:
            value += error.display_primary_key_fqn + ": "

        value += error.display_primary_key

        return value

    def _get_error_details(self, errors: List[ChalkError]) -> List[_TTableRow]:
        if not errors:
            return [
                (
                    "Error Message",
                    "Unfortunately the cause of this error is unknown. Please contact Chalk for support and provide the Revision ID or the Trace ID above.",
                )
            ]

        truncated_from = None
        if len(errors) > _MAX_ERRORS_TO_DISPLAY:
            truncated_from = len(errors)
            errors = errors[:_MAX_ERRORS_TO_DISPLAY]

        t_details_for_one_error = List[_TTableRow]
        grouped_details: Dict[int, t_details_for_one_error] = collections.defaultdict(list)
        for i, e in enumerate(errors):
            grouped_details[i].append((f"Error {i + 1}", e.message) if len(errors) > 1 else ("Error", e.message))
            if e.exception and e.exception.message:
                grouped_details[i].append((f"Exception", e.exception.message))
            if e.exception and e.exception.stacktrace:
                grouped_details[i].append((f"Stacktrace", e.exception.stacktrace))
            if val := self._get_pkey_display_value(e):
                grouped_details[i].append((f"Pkey", val))

        flattened_details = sum(list(grouped_details.values()), [])
        if truncated_from:
            flattened_details.append(
                ("Errors Truncated", f"Displaying only {_MAX_ERRORS_TO_DISPLAY} out of {truncated_from}")
            )

        return flattened_details

    def handle_and_raise_error(
        self,
        batch_report: BatchReport,
        main_task_id: TaskID,
        operation_display_type: str,
    ) -> None:
        all_errors = batch_report.all_errors or []
        if not all_errors and batch_report.error:
            # `all_errors` is added long after `error`.
            # We might be hitting old server code here,
            # make sure we can still talk to old server.
            all_errors.append(batch_report.error)

        panel = self.enclosure_panel
        main_progress = self.main_progress
        progress_table = cast(Table, self.enclosure_panel.renderable)

        self.handle_explainer_text_if_erring()
        panel.border_style = Style(color="red")
        main_progress.update(
            main_task_id,
            description=f"Error occurred while executing {operation_display_type}",
        )

        key_to_display_key = {
            _CHALK_TRACE_ID_KEY: "Trace ID",
        }

        metadata = batch_report.operation_metadata or {}
        if not isinstance(metadata, Mapping):
            metadata = {}

        metadata_tuples = [(key_to_display_key.get(k, k), v) for k, v in metadata.items()]
        failing_resolver = self._get_failing_resolver(batch_report)

        table_contents: List[_TTableRow] = [
            ("Revision ID", str(self.operation_id)),
            *metadata_tuples,
            *([("Failing Resolver", failing_resolver)] if failing_resolver else []),
            *self._get_error_details(all_errors),
        ]
        error_box = Table(
            box=box.SQUARE,
            show_lines=True,
            show_header=False,
            style=Style(color="red"),
            row_styles=[Style(color="red")] * len(table_contents),
        )

        for row in table_contents:
            error_box.add_row(*row)

        progress_table.add_row(Padding(Text(""), (0, 0, 1, 0)))
        progress_table.add_row(error_box)

        raise ChalkBaseException(
            trace_id=metadata.get(_CHALK_TRACE_ID_KEY),
            errors=all_errors if all_errors else None,
        )

    def handle_explainer_text_if_erring(self):
        if self.caller_method:
            self.explainer_text._text = [
                f"The computation for this `DatasetRevision` has failed. {self.caller_method} cannot be executed."
            ]
            self.explainer_text.style = Style(color="red")

    def handle_explainer_text_if_successful(self):
        if self.caller_method:
            self.explainer_text._text = [
                f"The computation for this `DatasetRevision` has completed. {self.caller_method} will be executed."
            ]
            self.explainer_text.style = Style(color="red")

    def poll_report(self) -> Iterable[BatchReport]:
        first_missing_report_dt = None
        poll_interval_seconds = 0.2
        report_missing_timeout = timedelta(minutes=1)

        while first_missing_report_dt is None or datetime.now() < first_missing_report_dt + report_missing_timeout:
            time.sleep(poll_interval_seconds)
            batch_report = self.client._get_batch_report(self.operation_id, self._environment_id)
            if batch_report is None:
                first_missing_report_dt = first_missing_report_dt or datetime.now()
            else:
                first_missing_report_dt = None
                self._operation_kind = batch_report.operation_kind
                yield batch_report
        else:
            raise TimeoutError(f"Timed out waiting for status report of operation with ID {self.operation_id}")

    def await_operation(self, show_progress: bool = False) -> None:
        if show_progress and get_console().is_dumb_terminal:
            _logger.warning("Progress display is not supported in dumb terminals. Progress will not be shown.")
            show_progress = False

        if show_progress:
            try:
                fqn_to_task_id = {}
                initial_description = "Starting query execution"
                main_task_id = self.main_progress.add_task(description=initial_description, total=1)
                main_task = self.main_progress._tasks[main_task_id]

                with ChalkLive(self.enclosure_panel, auto_refresh=True):
                    for batch_report in self.poll_report():
                        operation_display_type = _kind_to_display_type.get(batch_report.operation_kind, "Operation")

                        # Update main progress text
                        if main_task.description == initial_description:
                            description = (
                                f"Executing {operation_display_type}"
                                if self._operation_kind == BatchOpKind.RECOMPUTE
                                else f"Executing {operation_display_type}"
                            )
                            self.main_progress.update(main_task_id, description=description)

                        self.handle_resolver_update(batch_report=batch_report, fqn_to_task_id=fqn_to_task_id)

                        if batch_report.status == BatchOpStatus.COMPLETED:
                            self.handle_success(
                                main_task_id=main_task_id, operation_display_type=operation_display_type
                            )
                            break

                        if batch_report.status == BatchOpStatus.FAILED:
                            self.handle_and_raise_error(
                                batch_report=batch_report,
                                main_task_id=main_task_id,
                                operation_display_type=operation_display_type,
                            )
                            break  # should have raised but just in case
            except (TimeoutError, ChalkBaseException) as e:
                raise e
            except Exception:
                # If we get an exception, presumably due to progress bar rendering,
                # we fallback to not show progress bars, and keep polling.
                show_progress = False

        if not show_progress:
            for batch_report in self.poll_report():
                metadata = batch_report.operation_metadata or {}
                if not isinstance(metadata, Mapping):
                    metadata = {}

                if batch_report.status == BatchOpStatus.FAILED:
                    raise ChalkBaseException(
                        trace_id=metadata.get(_CHALK_TRACE_ID_KEY),
                        errors=batch_report.all_errors if batch_report.all_errors else None,
                    )
                if batch_report.status == BatchOpStatus.COMPLETED:
                    break
