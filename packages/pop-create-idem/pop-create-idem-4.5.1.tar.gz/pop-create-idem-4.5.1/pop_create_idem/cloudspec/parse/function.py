from typing import Dict
from typing import List

from cloudspec import CloudSpecFunction
from cloudspec import CloudSpecParam


def return_type(hub, func_data: CloudSpecFunction):
    ret = ""
    if func_data.return_type:
        ret += "\n\n    Returns:\n"
        ret += f"        {func_data.return_type}"
        ret += "\n"
    return ret


def doc(hub, func_data: CloudSpecFunction):
    if func_data.doc:
        doc = func_data.doc.replace('"""', "'''")
        doc = "\n" + hub.tool.format.wrap.indent(doc, 1) + "\n"
    else:
        doc = ""
    return doc


def parse(hub, functions: Dict[str, CloudSpecFunction], targets: List[str]):
    funcs = {}
    if not functions:
        # It might be an init file
        return funcs
    for function_name in targets:
        function_data = functions.get(function_name)
        # This lets us create partial plugin
        if function_data:
            # These known params should be first in the list of required params according to contract
            idem_known_params = {}
            # Add resource_id parameter
            if function_name in [
                "present",
                "absent",
                "get",
                "create",
                "update",
                "delete",
            ]:
                if (
                    "resource_id"
                    not in hub.cloudspec.parse.param.simple_map(
                        function_data.params
                    ).keys()
                ):
                    idem_known_params["resource_id"] = CloudSpecParam(
                        hub=hub,
                        name="resource_id",
                        doc=f"{function_data.hardcoded.get('resource_name', '').capitalize()} unique ID",
                        required=True
                        if function_name in ["update", "delete", "get"]
                        else False,
                        target="kwargs",
                        target_type="mapping",
                        param_type="str",
                        exclude_from_example=True,
                    )
                else:
                    # if it was already present, we will pop it into known param dict
                    idem_known_params["resource_id"] = function_data.params.pop(
                        "resource_id"
                    )

            # Add name parameter
            if function_name in [
                "present",
                "absent",
                "get",
                "list",
                "create",
                "update",
                "delete",
            ]:
                if (
                    "name"
                    not in hub.cloudspec.parse.param.simple_map(
                        function_data.params
                    ).keys()
                ):
                    idem_known_params["name"] = CloudSpecParam(
                        hub=hub,
                        name="name",
                        doc=f"Idem name of the resource.",
                        required=True
                        if function_name in ["present", "absent"]
                        else False,
                        target="kwargs",
                        target_type="mapping",
                        param_type="str",
                        exclude_from_example=True,
                    )
                else:
                    # if it was already present, we will pop it into known param dict
                    idem_known_params["name"] = function_data.params.pop("name")

            if idem_known_params and function_data.params:
                function_data.params = {**idem_known_params, **function_data.params}

            doc = hub.cloudspec.parse.function.doc(function_data)
            doc += hub.cloudspec.parse.param.sphinx_docs(function_data.params)
            doc += "\n\n    Returns:\n        Dict[str, Any]\n"

            if "absent" == function_name and function_data.params:
                # By idem's contract,
                #   - all absent function parameters except 'name' should not be required
                for param_name, metadata in function_data.params.items():
                    if param_name.lower() != "name":
                        metadata["required"] = False

            param_mapping = hub.cloudspec.parse.param.mappings(function_data.params)

            funcs[function_name] = dict(
                function=dict(
                    name=function_name,
                    hardcoded=function_data.hardcoded,
                    doc=doc,
                    header_params=hub.cloudspec.parse.param.headers(
                        function_data.params
                    ),
                    required_call_params=hub.cloudspec.parse.param.required_call_params(
                        function_data.params
                    ),
                ),
                parameter=dict(
                    mapping=param_mapping,
                ),
            )
    return funcs
