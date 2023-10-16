from typing import Any, List, Sequence, Tuple, Type, Union

from chalk import Resolver
from chalk.features import Feature, FeatureNotFoundException, FeatureSetBase, FeatureWrapper
from chalk.features.feature_set import Features, is_features_cls
from chalk.utils.string import to_snake_case


def encode_outputs(output: Sequence[Union[str, Any]]) -> Tuple[List[str], List[str]]:
    """Returns a list of encoded outputs and warnings"""
    all_warnings: List[str] = []
    encoded_output: List[str] = []
    for o in output:
        feature_fqns, warnings = encode_feature_or_resolver(o)
        all_warnings += warnings
        encoded_output += feature_fqns
    return encoded_output, all_warnings


def encode_feature_or_resolver(
    output_element: Union[Feature, FeatureWrapper, Type[Features], Resolver, str]
) -> Tuple[List[str], List[str]]:
    """
    Should gracefully warn and never error!
    Parameters
    ----------
    output_element:
        If Feature or FeatureWrapper, simply str() it
        If Type[Features], it is a FeatureSet. Will be feature-exploded engine side. Simply str() it.
        If Resolver, will be exploded to resolver outputs engine side. Return resolver.name
        If string, warn if it is not a Feature, FeatureSet, or a Resolver. Otherwise,
            call encode_feature_or_resolver() again.

    Returns
    -------
    encoded_output: a list of feature fqns or resolver names
    all_warnings: a list of str warnings
    """
    all_warnings: List[str] = []
    encoded_output: List[str] = []
    if isinstance(output_element, (Feature, FeatureWrapper)):
        encoded_output.append(str(output_element))
    elif is_features_cls(output_element):
        encoded_output.append(str(output_element))
    elif isinstance(output_element, Resolver):
        encoded_output.append(output_element.name)
    elif isinstance(output_element, str):
        feature_or_resolver_or_none = find_feature_or_resolver_by_fqn(output_element)
        if feature_or_resolver_or_none is None:
            all_warnings.append(
                f"Input '{output_element}' not recognized as feature or resolver. "
                + f"JSON encoding '{output_element}' and requesting anyways"
            )
            encoded_output.append(output_element)
        else:
            feature_fqns, warnings = encode_feature_or_resolver(feature_or_resolver_or_none)
            all_warnings += warnings
            encoded_output += feature_fqns
    else:
        all_warnings.append(
            f"Unrecognized type for {output_element}. " + f"JSON encoding '{output_element}' and requesting anyways"
        )
        encoded_output.append(str(output_element))
    return encoded_output, all_warnings


def find_feature_or_resolver_by_fqn(fqn: str) -> Union[Feature, Type[Features], Resolver, None]:
    """Returns feature if feature fqn, Type[Features] if feature namespace, resolver if resolver fqn, or None if neither
    Does not have to recurse on has-ones or has-manys"""
    for resolver in Resolver.registry:
        if resolver.name == fqn:
            return resolver

    if fqn in FeatureSetBase.registry:
        return FeatureSetBase.registry[fqn]
    try:
        feature = Feature.from_root_fqn(fqn)
        return feature
    except FeatureNotFoundException:
        return None
