from collections.abc import Mapping as MappingABC
from typing import Any, Dict, List, Mapping, Tuple

from chalk.features import Features, TPrimitive, ensure_feature
from chalk.features._encoding.json import unstructure_primitive_to_json
from chalk.features.feature_field import FeatureNotFoundException
from chalk.utils.json import TJSON


def _recursive_unstructure_primitive_to_json(val: TPrimitive) -> TJSON:
    if isinstance(val, MappingABC):
        return {k: _recursive_unstructure_primitive_to_json(v) for k, v in val.items()}
    elif isinstance(val, List):
        return [_recursive_unstructure_primitive_to_json(x) for x in val]
    else:
        return unstructure_primitive_to_json(val)


def recursive_encode_inputs(inputs: Mapping[str, Any]) -> Tuple[Dict[str, TJSON], List[str]]:
    all_warnings: List[str] = []
    encoded_inputs: Dict[str, TJSON] = {}
    for fqn, v in inputs.items():
        try:
            feature = ensure_feature(fqn)
        except FeatureNotFoundException:
            all_warnings.append(
                f"Input '{fqn}' not recognized. Recursively JSON encoding '{fqn}' and requesting anyways"
            )
            encoded_inputs[fqn] = _recursive_unstructure_primitive_to_json(v)
            continue

        if feature.is_has_many:
            if not isinstance(v, list):
                raise TypeError(f"has-many feature '{feature.fqn}' must be a list, but got {type(v).__name__}")

            has_many_result: List[Dict[str, TJSON]] = []
            assert feature.joined_class is not None
            foreign_namespace = feature.joined_class.namespace
            for item in v:
                # The value can be either a feature instance or a dict
                if isinstance(item, Features):
                    item = dict(item.items())
                if not isinstance(item, MappingABC):
                    raise TypeError(
                        (
                            f"Has-many feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                            f"but got a list of `{type(item).__name__}`"
                        )
                    )
                # Prepend the namespace onto the dict keys, if it's not already there
                item = {
                    k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                    for (k, sub_v) in item.items()
                }
                result, inner_warnings = recursive_encode_inputs(item)
                all_warnings.extend(inner_warnings)
                has_many_result.append(result)

            encoded_inputs[feature.root_fqn] = has_many_result
        elif feature.is_has_one:
            # The value can be either a feature instance or a dict
            assert feature.joined_class is not None
            foreign_namespace = feature.joined_class.namespace
            # The value can be either a feature instance or a dict
            if isinstance(v, Features):
                v = dict(v.items())
            if not isinstance(v, MappingABC):
                raise TypeError(
                    (
                        f"Has-one feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                        f"but got a list of `{type(v).__name__}`"
                    )
                )
            # Prepend the namespace onto the dict keys, if needed
            v = {
                k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                for (k, sub_v) in v.items()
            }
            has_one_values, inner_warnings = recursive_encode_inputs(v)
            all_warnings.extend(inner_warnings)
            # Flatten the has-one inputs onto the encoded inputs dict -- similar to how input
            # features
            root_parts = feature.root_fqn.split(".")
            for k, encoded_v in has_one_values.items():
                # Chop off the namespace from the nested features, as the
                # namespace is implied by the has-one feature
                root_fqn = ".".join((*root_parts, *k.split(".")[1:]))
                encoded_inputs[root_fqn] = encoded_v
        else:
            if feature.primary:
                if not isinstance(v, (int, str)):
                    raise TypeError(f"Input '{v}' for primary feature {feature.root_fqn} must be of type int or str")
            encoded_inputs[feature.root_fqn] = feature.converter.from_rich_to_json(
                v,
                missing_value_strategy="error",
            )

    return encoded_inputs, all_warnings
