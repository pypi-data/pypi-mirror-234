"""Parse parameters related metadata"""
from typing import Dict

import openapi3

__func_alias__ = {"type_": "type"}


def parse_schema_members(hub, params: dict, schema_ref: str, all_schemas: dict):
    """
    Resolve "#/components/schema/Pet type of schema into parameters
    """
    if not schema_ref:
        return

    parameters: list = all_schemas.get(schema_ref)
    if parameters:
        for p in parameters:
            doc = p.get("description")
            nested_member = {}
            if p.get("nested_member", None):
                # parse nested members
                nested_params = {}
                hub.pop_create.openapi3.params.parse_schema_members(
                    nested_params, p.get("nested_member"), all_schemas
                )

                if nested_params.get("primitive", None):
                    param_type = nested_params.get("primitive", {}).get("param_type")
                    doc = nested_params.get("primitive", {}).get("doc")
                else:
                    param_type = hub.pop_create.openapi3.params.type(
                        p.get("type"), p.get("member_type", None)
                    )
                    nested_member = {
                        "name": p.get("idem_name"),
                        "params": nested_params,
                    }
            else:
                param_type = hub.pop_create.openapi3.params.type(
                    p.get("type"), p.get("member_type", None)
                )

            params[p.get("idem_name")] = {
                "required": p.get("required", False),
                "target_type": "mapping",
                "target": "kwargs",
                "param_type": param_type,
                "doc": doc,
            }

            if nested_member:
                params[p.get("idem_name")]["member"] = nested_member


def parse_non_schema_members(hub, parameter: openapi3.paths.Parameter):
    """
    Resolve query, path, header or cookie type of inputs into parameters
    """
    if parameter.in_ == "query":
        target_type = "mapping"
    elif parameter.in_ == "path":
        target_type = "mapping"
    elif parameter.in_ == "header":
        target_type = "mapping"
    elif parameter.in_ == "cookie":
        target_type = "mapping"
    else:
        raise ValueError(f"Unknown parameter type: {parameter.in_}")

    return {
        "required": parameter.required,
        "target_type": target_type,
        "target": parameter.in_,
        "param_type": hub.pop_create.openapi3.params.type(
            parameter.schema.type
            if isinstance(parameter.schema, openapi3.schemas.Schema)
            else None,
            parameter.schema.items.type if parameter.schema.items else None,
        ),
        "doc": parameter.description,
    }


def parse_resource_to_request_input_mappings(hub, schema_ref: str, all_schemas: dict):
    resource_to_request_input_mapping = {}
    if not schema_ref:
        return "{}"

    parameters: list = all_schemas.get(schema_ref)
    if parameters:
        for p in parameters:
            if "idem_name" in p and p.get("idem_name"):
                resource_to_request_input_mapping[p.get("idem_name")] = p.get(
                    "actual_name", ""
                )

    # This is used when mapping idem formatted resource attributes to raw request inputs
    # resource_to_request_input_mapping = {
    #     "photo_urls": "photoUrls", -> photoUrls is the attribute on server side but idem name is snaked as photo_urls
    #     "tags": tags,
    # }
    return resource_to_request_input_mapping


def parse_response_mappings(hub, schema_ref: str, all_schemas: dict) -> Dict[str, str]:
    """
    Resolve idem_resource to request payload
    """
    response_mapping = {}
    if not schema_ref:
        return response_mapping

    parameters: list = all_schemas.get(schema_ref)
    if parameters:
        # e.g. a get pet request would get the following (raw: present) response mapping
        # {
        #     "category": "category",
        #     "id": "id",
        #     "name": "name",
        #     "photoUrls": "photo_urls"
        #     "status": "status",
        #     "tags": "tags",
        # }
        for p in parameters:
            if "actual_name" in p and p.get("actual_name"):
                response_mapping[p.get("actual_name")] = p.get("idem_name", "")

    return response_mapping


def type_(hub, param_type: str, param_member_type: str) -> str:
    if "integer" == param_type:
        return "int"
    elif "boolean" == param_type:
        return "bool"
    elif "number" == param_type:
        return "float"
    elif "string" == param_type:
        return "str"
    elif "array" == param_type:
        if param_member_type:
            return (
                f"List[{hub.pop_create.openapi3.params.type(param_member_type, None)}]"
            )
        else:
            return "List"
    elif "object" == param_type:
        return "Dict"
    elif "nested" == param_type:
        # This translates into makedataclass
        return "{}"
    elif "nested_array" == param_type:
        # This translates into List[makedataclass]
        return "List[{}]"
    else:
        return ""
