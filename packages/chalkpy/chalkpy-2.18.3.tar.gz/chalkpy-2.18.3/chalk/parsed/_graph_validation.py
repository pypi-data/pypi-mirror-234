from __future__ import annotations

import collections
from collections import defaultdict
from typing import DefaultDict, Dict, List, Mapping

from chalk.parsed.duplicate_input_gql import (
    GraphLogSeverity,
    ProjectSettingsGQL,
    UpdateGraphError,
    UpsertFeatureGQL,
    UpsertGraphGQL,
    UpsertResolverGQL,
)
from chalk.utils import string
from chalk.utils.duration import parse_chalk_duration
from chalk.utils.string import oxford_comma_list, to_camel_case


class _LogBuilder:
    def __init__(self):
        self._logs: List[UpdateGraphError] = []

    def add_log(self, header: str, subheader: str, severity: GraphLogSeverity):
        self._logs.append(UpdateGraphError(header=header, subheader=subheader, severity=severity))

    def add_error(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.ERROR)

    def add_warning(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.WARNING)

    def add_info(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.INFO)

    def get_logs(self) -> List[UpdateGraphError]:
        return self._logs


def _validate_primary_key(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if (
        feature.scalarKind is not None
        and feature.scalarKind.primary
        and feature.scalarKind.scalarKind not in ["str", "int"]
    ):
        builder.add_error(
            header=f'Invalid primary key type "{feature.id.fqn}"',
            subheader=(
                f"Primary keys must be integers or strings. "
                f'Feature "{feature.id.fqn}" has a type of {feature.scalarKind.scalarKind}'
            ),
        )


def _validate_max_staleness(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.maxStaleness is not None and feature.maxStaleness != "infinity":
        try:
            parse_chalk_duration(feature.maxStaleness)
        except:
            builder.add_error(
                header=f'Could not parse max_staleness for feature "{feature.id.fqn}"',
                subheader=f'Received "{feature.maxStaleness}". See https://docs.chalk.ai/docs/duration for valid formats.',
            )


def _validate_etl_to_online(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.etlOfflineToOnline and feature.maxStaleness is None:
        builder.add_error(
            header=f'Missing max staleness for "{feature.id.fqn}"',
            subheader=f'The feature "{feature.id.fqn}" is set to ETL to online, but doesn\'t specify a max staleness. Any ETL to online would be immediately invalidated.',
        )


def _validate_no_feature_times_as_input(
    fqn_to_feature: Mapping[str, UpsertFeatureGQL],
    resolver: UpsertResolverGQL,
    builder: _LogBuilder,
):
    for i in resolver.inputs or []:
        if i.underlying.fqn not in fqn_to_feature:
            builder.add_error(
                header=f'Resolver "{resolver.fqn}" an unknown feature {i.underlying.fqn}',
                subheader=f"""Please check the inputs to this resolver, and make sure they are all features.""",
            )
        elif fqn_to_feature[i.underlying.fqn].featureTimeKind is not None and resolver.kind != "offline":
            builder.add_error(
                header=f"Feature times cannot be accepted as input to {resolver.kind} resolvers.",
                subheader=(
                    f'The resolver "{resolver.fqn}" takes as input the\n'
                    f'feature "{i.underlying.fqn}", a feature_time() type.\n'
                    f"Feature times can be returned from {resolver.kind} resolvers to\n"
                    "indicate data from the past, but cannot be accepted\n"
                    "as inputs."
                ),
            )


def _validate_feature_names_unique(features: List[UpsertFeatureGQL], builder: _LogBuilder):
    counter: DefaultDict[str, int] = defaultdict(lambda: 0)
    for r in features:
        counter[r.id.fqn] += 1

    for fqn, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate feature names",
                subheader=(
                    f'There are {count} features with the same name of "{fqn}". All features require a '
                    f"distinct name"
                ),
            )


def _validate_resolver_names_unique(resolvers: List[UpsertResolverGQL], builder: _LogBuilder):
    counter: DefaultDict[str, int] = defaultdict(lambda: 0)
    for r in resolvers:
        counter[r.fqn.split(".")[-1]] += 1

    for name, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate resolver names",
                subheader=(
                    f'There are {count} resolvers with the same name of "{name}". All resolvers require a '
                    f"distinct name"
                ),
            )


def _validate_offline_resolver_has_one(resolver: UpsertResolverGQL, builder: _LogBuilder):
    if resolver.kind != "offline":
        return

    for i in resolver.inputs or []:
        if i.path is not None and len(i.path) > 1:
            full_path = [i.path[0].parent.fqn]
            for p in i.path[1:]:
                full_path.append(p.child.namespace)
            full_path.append(i.path[-1].parentToChildAttributeName)
            pathname = ".".join(full_path)
            builder.add_error(
                header="Invalid offline resolver input",
                subheader=(
                    "Offline resolvers cannot require nested of more than one level. "
                    f'The resolver "{resolver.fqn}" takes as input the feature "{pathname}".'
                ),
            )


def _validate_resolver_input(
    singleton_namespaces: set[str],
    resolver: UpsertResolverGQL,
    builder: _LogBuilder,
):
    namespaces = set()

    for i in resolver.inputs or []:
        f = i.path[0].parent if i.path is not None and len(i.path) > 0 else i.underlying
        if f.namespace not in singleton_namespaces:
            namespaces.add(f.namespace)

    namespaces = list(namespaces)
    if len(namespaces) > 1:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" requires features from multiple namespaces.',
            subheader=f"""All inputs to a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" takes inputs in the namespaces {oxford_comma_list(string.add_quotes(namespaces))}.

If you require features from many feature classes, reference them via their relationships, such as:
  User.bank_account.title,
  User.full_name

{resolver.functionDefinition}
""",
        )


def _validate_resolver_output(resolver: UpsertResolverGQL, builder: _LogBuilder):
    output = resolver.output
    features = output.features or []
    dataframes = output.dataframes or []
    if len(features) == 0 and len(dataframes) == 0:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" does not define outputs.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    if len(dataframes) > 1:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" defines multiple DataFrames as output.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    if len(features) > 0 and len(dataframes) > 0:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" returns both relationships and scalar features.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    # Want to validate this but only have feature id instead of feature
    # if len(resolver.inputs) == 0 and len(dataframes) == 1 and len([pkey for pkey in dataframes[0].columns if pkey.primary]) != 1:
    #     builder.add_error(
    #         header=f'Resolver "{resolver.fqn}" must return a primary feature',
    #         subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
    #     )

    # Bring this back.


#     if len(features) > 0:
#         namespaces = list(set(f.namespace for f in features))
#         if len(namespaces) > 1:
#             builder.add_error(
#                 header=f'Resolver "{resolver.fqn}" outputs features from multiple namespaces.',
#                 subheader=f"""All outputs of a resolver should be rooted in the same namespace.
# The resolver "{resolver.fqn}" outputs features in the namespaces {oxford_comma_list(namespaces)}.
# See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.
#
# {resolver.functionDefinition}
# """,
#             )


# FIXME CHA-66 we should validate that joins are all pkey on pkey joins. no non-primary keys, no self-joins, no constants
def _validate_joins(feature: UpsertFeatureGQL, builder: _LogBuilder):
    pass


def _validate_feature_names(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.id.name.startswith("__") or feature.id.name.startswith("_chalk"):
        builder.add_error(
            header="Feature uses protected name",
            subheader=(
                f'The feature "{feature.id.fqn}" uses the protected name "{feature.id.name}". '
                'Feature names cannot begin with "_chalk" or "__". Please rename this feature.'
            ),
        )
    if feature.id.namespace.startswith("__") or feature.id.namespace.startswith("_chalk"):
        builder.add_error(
            header="Feature class uses protected namespace",
            subheader=(
                f'The feature "{feature.id.fqn}" belongs to the protected namespace "{feature.id.namespace}". '
                f'Feature namespaces cannot begin with "_chalk" or "__". Please rename this feature set.'
            ),
        )


def _validate_resolver_feature_cycles(
    fqn_to_feature: Mapping[str, UpsertFeatureGQL],
    resolver: UpsertResolverGQL,
    builder: _LogBuilder,
):
    input_root_fqns: set[str] = set()
    for inp in resolver.inputs or []:
        if fqn_to_feature[inp.underlying.fqn].scalarKind and not fqn_to_feature[inp.underlying.fqn].scalarKind.primary:
            if not inp.path:
                input_root_fqns.add(inp.underlying.fqn)
            else:
                path_parsed: List[str] = []
                path_parsed.append(inp.path[0].parent.namespace)
                path_parsed.append(inp.path[0].parent.name)
                for x in inp.path:
                    path_parsed.append(x.child.name)
                input_root_fqns.add(".".join(path_parsed))
        # FIXME: Validate cycles for has-one and has-many features

    output_features = list(resolver.output.features or [])
    output_features += [f for df in resolver.output.dataframes for f in (df.columns or [])]
    output_fqns: set[str] = set()
    for f in output_features:
        fqn = f"{f.namespace}.{f.name}"
        root_fqn = f.fqn  # for output features, the fqn is the root fqn
        if fqn_to_feature[fqn].scalarKind is not None and not fqn_to_feature[fqn].scalarKind.primary:
            output_fqns.add(root_fqn)

    shared_features = output_fqns & input_root_fqns
    if len(shared_features) > 0:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" has the same feature in its input and output (i.e. a cycle).',
            subheader=f"""The inputs and outputs of a resolver can't contain the same exact feature.
The resolver "{resolver.fqn}" contains the following shared features in its inputs and outputs: {sorted(shared_features)}
""",
        )


def _validate_resolver_input_and_output_namespace(resolver: UpsertResolverGQL, builder: _LogBuilder):
    input_features = [i.underlying for i in (resolver.inputs or [])]
    output_features = resolver.output.features or []
    all_features = input_features + output_features
    all_namespaces = {f.namespace for f in all_features}
    if len(all_namespaces) > 1:
        builder.add_warning(
            header=f'Resolver "{resolver.fqn}" has output and input features from multiple namespaces.',
            subheader=f"""All outputs and inputs of a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" references features in the namespaces {oxford_comma_list(sorted(all_namespaces))}.
See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.
""",
        )


_BUILT_IN_SUPPORTED_TYPES = {
    "datetime",
    "date",
    "int",
    "float",
    "str",
    "bool",
    "Enum",
    "__dataclass__",
    "__attrs__",
    "__pydantic__",
}

MissingMetadata = Dict[GraphLogSeverity, List[str]]


def _validate_feature_metadata(
    features: List[UpsertFeatureGQL],
    builder: _LogBuilder,
    request_config: ProjectSettingsGQL,
):
    class WrappedFeature:
        def __init__(self, feature: UpsertFeatureGQL, missing_metadata: MissingMetadata):
            self.feature = feature
            self.missing_metadata = missing_metadata

    def get_missing_metadata(feature: UpsertFeatureGQL) -> MissingMetadata:
        res: MissingMetadata = collections.defaultdict(list)
        if (
            request_config.validation
            and request_config.validation.feature
            and request_config.validation.feature.metadata
        ):
            settings = request_config.validation.feature.metadata
        else:
            settings = []
        for setting in settings:
            metadata_name = setting.name
            severity = GraphLogSeverity(setting.missing.upper())
            if hasattr(feature, metadata_name):
                value = getattr(feature, metadata_name)
                is_missing = value is None or (isinstance(value, list) and len(value) == 0)
                if is_missing:
                    res[severity].append(metadata_name)

        return res

    def get_missing_metadata_log(wrapped_features: List[WrappedFeature], severity: GraphLogSeverity):
        if not wrapped_features:
            return None, None

        missing_messages = []
        feature_str = "feature"
        missing_metadata_header_str = "missing metadata"
        max_name_len = max([len(w.feature.id.name) for w in wrapped_features])
        feature_column_width = max(max_name_len, len(feature_str)) + 1
        get_padding = lambda s: feature_column_width - len(s)

        first_feature = wrapped_features[0].feature
        header = f'"{to_camel_case(first_feature.id.namespace)}" features have missing metadata'
        subheader = f"  Filepath: {first_feature.namespacePath}\n\n"

        for wrapper in wrapped_features:
            missing_metadata = wrapper.missing_metadata.get(severity)
            if not missing_metadata:
                continue
            padding_1 = get_padding(wrapper.feature.id.name)
            missing_metadata_str = ", ".join(missing_metadata)
            missing_messages.append(f"      {wrapper.feature.id.name}{' ' * padding_1}: {missing_metadata_str}")

        if not missing_messages:
            return None, None

        padding_2 = get_padding(feature_str)
        subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
        subheader += f"      {feature_str}{' ' * padding_2}  {missing_metadata_header_str}\n"
        subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_header_str)}\n"
        subheader += "\n".join(missing_messages)

        return header, subheader

    def build_log_for_each_severity(wrapped_features: List[WrappedFeature]):
        if not wrapped_features:
            return

        for severity in GraphLogSeverity:
            header, subheader = get_missing_metadata_log(
                wrapped_features=wrapped_features, severity=GraphLogSeverity(severity)
            )
            if header is None or subheader is None:
                continue
            builder.add_log(header=header, subheader=subheader, severity=GraphLogSeverity(severity))

    def get_wrapped_features(
        namespace_features: List[UpsertFeatureGQL],
    ) -> List[WrappedFeature]:
        wrapped_features = []
        for nf in namespace_features:
            missing_metadata = get_missing_metadata(nf)
            if not missing_metadata:
                continue
            wrapped_features.append(WrappedFeature(feature=nf, missing_metadata=missing_metadata))

        return wrapped_features

    if not (
        request_config
        and request_config.validation
        and request_config.validation.feature
        and request_config.validation.feature.metadata
    ):
        return

    namespace_to_features = collections.defaultdict(list)
    for f in features:
        namespace_to_features[f.id.namespace].append(f)

    for ns_features in namespace_to_features.values():
        wf = get_wrapped_features(namespace_features=ns_features)
        build_log_for_each_severity(wrapped_features=wf)


def _validate_feature_metadata_config(
    features: List[UpsertFeatureGQL],
    builder: _LogBuilder,
    request_config: ProjectSettingsGQL,
):
    if not (
        request_config
        and request_config.validation
        and request_config.validation.feature
        and request_config.validation.feature.metadata
    ):
        return

    severities_lower = [e.lower() for e in GraphLogSeverity]
    first_feature = features and features[0]

    for missing_metadata in request_config.validation.feature.metadata:
        metadata_name = missing_metadata.name
        severity = missing_metadata.missing

        severity_upper = severity.upper()
        try:
            GraphLogSeverity(severity_upper)
        except ValueError:
            severity_choices = '" or "'.join(severities_lower)
            builder.add_warning(
                header=f'Found invalid log severity "{severity}" config for missing metadata',
                subheader=(
                    f'The required feature metadata "{metadata_name}" is associated with an invalid log severity "{severity}".'
                    f' Please use "{severity_choices}" in chalk.yml'
                ),
            )

        if first_feature and not hasattr(first_feature, metadata_name):
            builder.add_warning(
                header=f'Found invalid feature metadata "{metadata_name}" in config',
                subheader=(
                    f'The required metadata "{metadata_name}" is not a valid feature metadata.'
                    f" Please consider removing it from chalk.yml"
                ),
            )


def _validate_namespace_primary_key(
    namespace: str,
    features: List[UpsertFeatureGQL],
    builder: _LogBuilder,
    singleton_namespaces: set[str],
):
    if namespace in singleton_namespaces:
        return

    primary_features = list(f for f in features if f.scalarKind and f.scalarKind.primary)

    if len(primary_features) == 0:
        builder.add_error(
            header=f"Feature set '{namespace}' is missing a primary feature",
            subheader=f"Please add an 'int' or 'str' feature to '{namespace}', annotated with '= feature(primary=True)'",
        )
    elif len(primary_features) > 1:
        names = ", ".join([f.id.name for f in primary_features])
        builder.add_error(
            header=f"Feature set '{namespace}' has too many primary features",
            subheader=f"Found primary features: {names}. Composite primary keys are not supported. Please mark only a single feature as primary.",
        )


def validate_graph(request: UpsertGraphGQL) -> List[UpdateGraphError]:
    singleton_namespaces = {c.name for c in request.featureClasses or [] if c.isSingleton}
    builder = _LogBuilder()

    # Validate the features
    _validate_feature_names_unique(request.features or [], builder)
    _validate_feature_metadata(request.features or [], builder, request.config)
    _validate_feature_metadata_config(request.features or [], builder, request.config)

    namespaces: Dict[str, List[UpsertFeatureGQL]] = defaultdict(list)

    for feature in request.features or []:
        namespaces[feature.id.namespace].append(feature)

    for namespace, features in namespaces.items():
        _validate_namespace_primary_key(
            namespace=namespace,
            features=features,
            builder=builder,
            singleton_namespaces=singleton_namespaces,
        )

    for feature in request.features or []:
        _validate_primary_key(feature, builder)
        _validate_max_staleness(feature, builder)
        _validate_joins(feature, builder)
        _validate_etl_to_online(feature, builder)
        _validate_feature_names(feature, builder)

    # Validate the resolvers
    fqn_to_feature = {f.id.fqn: f for f in request.features or []}

    _validate_resolver_names_unique(request.resolvers or [], builder)
    for resolver in request.resolvers or []:
        _validate_offline_resolver_has_one(resolver, builder)
        _validate_resolver_input(
            singleton_namespaces=singleton_namespaces,
            resolver=resolver,
            builder=builder,
        )
        _validate_resolver_output(resolver, builder)
        _validate_resolver_feature_cycles(fqn_to_feature=fqn_to_feature, resolver=resolver, builder=builder)
        # TODO Some customers currently still do stuff like:
        # >>> def some_resolver(uid: User.id) -> DataFrame[Transaction]: ....
        # So don't even warn about it
        # _validate_resolver_input_and_output_namespace(resolver, builder)
        _validate_no_feature_times_as_input(
            fqn_to_feature=fqn_to_feature,
            resolver=resolver,
            builder=builder,
        )

    return builder.get_logs()
