import yaml


def state_request_syntax(
    hub, resource_name: str, ref: str, func_name: str, params: dict
):
    example_params = hub.cloudspec.parse.example.extract_params(params)
    request_syntax = {
        f"idem_test_{resource_name}_is_{func_name}": {
            f"{ref}.{func_name}": [
                {key: value} for key, value in example_params.items()
            ]
        }
    }

    return _display(request_syntax)


def extract_params(hub, params: dict):
    result = {}
    for name, param in params.items():
        if param.get("exclude_from_example"):
            continue

        snaked = param.get("snaked")
        param_type = param.get("param_type")
        if param_type == "str":
            param_type = "string"

        if param.get("member", None):
            if param_type == "List[{}]":
                result[snaked] = [
                    hub.cloudspec.parse.example.extract_params(
                        param.get("member", {}).get("params")
                    )
                ]
            elif param_type == "{}":
                result[snaked] = hub.cloudspec.parse.example.extract_params(
                    param.get("member", {}).get("params")
                )
        else:
            if param_type == "list" or param_type == "List[str]":
                result[snaked] = ["value"]
            elif param_type == "Dict[str, str]" or param_type == "Dict[str, {}]":
                result[snaked] = ["key : value"]
            else:
                result[snaked] = param_type

    return result


def _display(data):
    """
    Print the raw data
    Disclaimer: This is taken from https://gitlab.com/vmware/pop/rend/-/blob/master/rend/output/yaml_out.py
    """

    # # yaml safe_dump doesn't know how to represent subclasses of dict.
    # # this registration allows arbitrary dict types to be represented
    # # without conversion to a regular dict.
    def any_dict_representer(dumper, data):
        return dumper.represent_dict(data)

    yaml.add_multi_representer(dict, any_dict_representer, Dumper=yaml.SafeDumper)
    return yaml.safe_dump(data)
