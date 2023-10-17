import re
from typing import Dict

from cloudspec import CloudSpecParam


def sphinx_docs(hub, parameters: CloudSpecParam) -> str:
    """
    Get the sphinx docs for the parameters
    """
    if not parameters:
        return ""

    ret = "\n    Args:\n"

    # Add required params first
    for name, data in parameters.items():
        if data["required"]:
            ret += add_param_to_sphynx_doc(data)

    # Add not required params after
    for name, data in parameters.items():
        if not data["required"]:
            ret += add_param_to_sphynx_doc(data)

    return ret.rstrip()


def add_param_to_sphynx_doc(param: CloudSpecParam):
    ret = f"        {param.snaked}"
    # Doc strings standard is lower case list[]
    if param.param_type is None:
        param_type = None
    else:
        param_type = param.param_type.replace("list[", "list[")
    if param.member:
        # Complex params are represented as Dict[str, Any] in the sphinx docs
        param_type = param_type.format("dict[str, Any]")

    if param_type:
        ret += f"({param_type}{', Optional' if not param.required else ''})"

    # vRA idem resource provider parsing logic expects parameter doc to be defined on new line
    # If parameter doc has new lines, make sure that every new line is followed by the offset
    doc_offset = "            "
    ret += f":\n{param.doc}".replace("\n", "\n" + doc_offset)

    if not re.search(r"[ .\n]$", ret):
        ret += "."
    if not ret.endswith(" "):
        ret += " "
    if not param.required:
        ret += f"Defaults to {param.default}."

    ret += nested_params_docs(param, "            ")
    ret += "\n\n"
    return ret


def nested_params_docs(param: CloudSpecParam, offset: str):
    """
    Get the sphinx docs for the nested parameters
    """
    ret = ""
    if param.member:
        for nested_param_name, nested_param_data in param.member.params.items():
            # Doc strings standard is lower case list[]
            param_type = nested_param_data.param_type.replace("list[", "list[")
            if nested_param_data.member:
                # This is the next level of nested complex argument.
                param_type = param_type.format("dict[str, Any]")
            # vRA idem resource provider doc parsing logic expects nested properties to be prefixed with *
            ret += f"\n\n{offset}* "

            ret += f"{nested_param_name} ({param_type}{', Optional' if not nested_param_data.required else ''})"
            # vRA idem resource provider doc parsing logic expects parameter doc to be defined on new line
            # If parameter doc has new lines, make sure that every new line is followed by the offset
            doc_offset = f"{offset}    "
            ret += f":\n{nested_param_data.doc}".replace("\n", "\n" + doc_offset)

            if not re.search(r"[ .\n]$", ret):
                ret += "."
            if not ret.endswith(" "):
                ret += " "
            if not nested_param_data.required:
                ret += f"Defaults to {param.default}."

            # Recursively add doc for all nested complex arguments
            ret += nested_params_docs(nested_param_data, offset + "    ")
    return ret


def headers(hub, parameters: CloudSpecParam) -> str:
    """
    The arguments that will be put in the function definition
    """
    ret = ""

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_name, param_data in required_params.items():
        ret += add_param_to_header(param_data)

    unrequired_params = {
        name: data for name, data in parameters.items() if not data["required"]
    }

    for param_name, param_data in unrequired_params.items():
        ret += add_param_to_header(param_data)

        # TODO handle this case properly
        if param_data.default == "{}" or param_data.default == "[]":
            ret += f" = None"
        else:
            ret += f" = {param_data.default}"

    return ret


def add_param_to_header(param_data: Dict) -> str:
    ret = f",\n    {param_data.snaked}: "
    if param_data.member:
        # Insert nested complex format for as the argument type.
        # param_type should be "{}|List[{}]|Dict[str, {}]"
        ret += f"{param_data.param_type}".format(
            add_nested_param_to_header(param_data.member, "        ")
        )
    else:
        ret += f"{param_data.param_type}"

    return ret


def add_nested_param_to_header(member: Dict, offset: str) -> str:
    """
    Create a dataclass for a complex nested argument
    """
    ret = f'make_dataclass(\n{offset}"{member.name}",\n{offset}['
    required_params = {
        name: data for name, data in member.get("params").items() if data["required"]
    }

    for param_name, param_data in required_params.items():
        ret += add_nested_param(param_name, param_data, offset)

    unrequired_params = {
        name: data
        for name, data in member.get("params").items()
        if not data["required"]
    }

    for param_name, param_data in unrequired_params.items():
        ret += add_nested_param(param_name, param_data, offset)

    # Remove last ', '
    ret = ret[0:-2]
    ret += f"\n{offset}]\n{offset})"

    return ret


def add_nested_param(param_name: str, param_data, offset: str):
    ret = ""
    ret += f"\n{offset}    "
    # TODO: Nested param name should be snaked
    ret += f'("{param_name}", '
    if param_data.member:
        # Recursively add all nested complex arguments
        ret += param_data.param_type.format(
            add_nested_param_to_header(param_data.member, offset + "    ")
        )
    else:
        ret += f"{param_data.param_type}"

    if param_data["required"]:
        ret += f"), "
    elif param_data.param_type == "int" and param_data.default == 0:
        # Since idem 23.0.3 the default values are populated automatically and value of 0 may fail.
        ret += f", field(default=None)), "
    else:
        ret += f", field(default={param_data.default})), "

    return ret


def required_call_params(hub, parameters: CloudSpecParam) -> str:
    """
    Get a mapping of required function args to the values that will be used in the final caller
    """
    ret = []

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_data in required_params.values():
        ret.append(f"{param_data.snaked}={param_data.default or 'value'}")

    return ", ".join(ret)


def all_call_params(hub, parameters: CloudSpecParam) -> str:
    """
    Get a mapping of all function args to the values that will be used in the final caller
    """
    ret = []

    all_params = {name: data for name, data in parameters.items()}
    for param_data in all_params.values():
        ret.append(f"{param_data.snaked}={param_data.default or 'value'}")

    return ", ".join(ret)


def mappings(hub, parameters: CloudSpecParam) -> Dict[str, str]:
    ret = {}
    map_params = {
        name: data
        for name, data in parameters.items()
        if data["target_type"] == "mapping"
    }
    for name, data in map_params.items():
        target = data["target"]
        if target not in ret:
            ret[target] = {}
        ret[target][name] = data.snaked

    fmt = lambda item: ", ".join(f'"{k}": {v}' for k, v in item.items())
    return {k: f"{{{fmt(v)}}}" for k, v in ret.items()}


def simple_map(hub, parameters: Dict[str, CloudSpecParam]):
    result = {}
    for k, param_data in parameters.items():
        if k == "name" and param_data.target_type == "arg":
            continue
        result[param_data.snaked] = k
    return result
