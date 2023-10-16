from typing import Iterable, Optional, Sequence, Tuple

from prodvana.proto.prodvana.common_config.parameters_pb2 import (
    ParameterDefinition,
    ParameterValue,
)


def make_default_value(param_def: ParameterDefinition) -> Optional[ParameterValue]:
    val = ParameterValue(name=param_def.name)
    if param_def.int:
        val.int = param_def.int.default_value
    elif param_def.string:
        val.string = param_def.string.default_value
    elif param_def.docker_image:
        val.docker_image_tag = param_def.docker_image.default_tag
    elif param_def.secret:
        return None  # no valid default value
    else:
        raise Exception(f"Unknown parameter definition: {param_def}")
    return val


def get_parameter_values(
    defs: Sequence[ParameterDefinition], values: Sequence[ParameterValue]
) -> Iterable[Tuple[ParameterDefinition, ParameterValue]]:
    """
    Given a list of parameter definitions and values, return a tuple of definitions with their values,
    where if no explicit value is provided, the default is used.

    If the parameter is required but no value is provided, that parameter is skipped (this is an invalid state).
    """
    val_by_name = {v.name: v for v in values}
    for param_def in defs:
        val = val_by_name.get(param_def.name)
        if not val:
            val = make_default_value(param_def)
        if not val:
            continue
        yield (param_def, val)
