import openapi3


def parse(hub, api: openapi3.OpenAPI):
    schemas = {}

    # Sometimes a schema could just point to different schema object
    # Let's hold them into a separate mapping for adding them into flat schema structure
    transitive_schema_mappings = {}
    # Get a flat structure for schemas

    complex_schema = {}

    # Let's build the reference mapping for complex schema
    for object_name, param in api.components.raw_element.get("schemas").items():
        if "allOf" in param:
            # Get everything as flattened
            complex_schema[object_name] = _resolve_complex_schema(param)
            # Add this in schema mappings so that it can be appended
            transitive_schema_mappings[
                f"#/components/schemas/{object_name}"
            ] = complex_schema[object_name].get("$ref")

    for object_name, param in api.components.raw_element.get("schemas").items():
        parameters = []

        if object_name in complex_schema:
            # Get all the parameters from a resolved 'allOf'
            param = complex_schema[object_name]

        if param.get("$ref", None):
            # It will be resolved later
            transitive_schema_mappings[
                f"#/components/schemas/{object_name}"
            ] = param.get("$ref")

        if param.get("type", "") == "object":
            # "StoreOrder": {
            #     "type": "object",
            #     "properties": {
            #         "name": {
            #             "type": "string",
            #             "description": ""
            #         },
            #     }
            for prop_name, prop_value in param.get("properties", {}).items():
                # Check for nested members first
                # "pet_order": {
                #    "$ref": "#/components/schemas/StoreOrder"
                #  },
                nested_member_ref = prop_value.get("$ref")
                nested_member_ref_type = "nested" if nested_member_ref else None
                if "array" == prop_value.get("type"):
                    # "tags": {
                    #     "type": "array",
                    #     "items": {
                    #         "$ref": "#/definitions/Tag"
                    #     }
                    # },
                    # "photoUrls": {
                    #     "type": "array",
                    #     "items": {
                    #         "type": "string",
                    #     }
                    # },
                    nested_member_ref = prop_value.get("items", {}).get("$ref")
                    # Keeping the default array for now so that it is becomes a list in function params
                    nested_member_ref_type = (
                        "nested_array" if nested_member_ref else "array"
                    )

                param_type = (
                    nested_member_ref_type
                    if nested_member_ref_type
                    else prop_value.get("type")
                )

                parameters.append(
                    dict(
                        idem_name=hub.tool.format.case.snake(prop_name),
                        actual_name=prop_name,
                        required=prop_name in param.get("required", []),
                        type=param_type,
                        member_type=prop_value.get("items", {}).get("type", None)
                        if "array" == param_type
                        else None,
                        nested_member=nested_member_ref,
                        description=prop_value.get("description") or prop_name,
                    )
                )
        else:
            # We may need to sanitize it later
            # "InventoryOrderStatus": {
            #     "type": "string",
            #     "description": "<>",
            # },
            parameters.append(
                dict(
                    idem_name="primitive",
                    type=param.get("type"),
                    description=param.get("description"),
                )
            )

        schemas[f"#/components/schemas/{object_name}"] = parameters

    for key, actual_schema_ref in transitive_schema_mappings.items():
        # Update schemas with actual schema reference
        _, object_name = key.split("/")[-2:]
        if object_name in complex_schema and key in schemas:
            schemas[key].extend(schemas[actual_schema_ref])
        else:
            schemas[key] = schemas[actual_schema_ref]

    return schemas


def _resolve_complex_schema(schema_obj):
    if isinstance(schema_obj, dict):
        if "allOf" in schema_obj:
            resolved_properties = {}
            for schema in schema_obj["allOf"]:
                # resolve allOf for each item in the allOf array
                resolved_properties.update(_resolve_complex_schema(schema))

            # Remove the allOf keyword
            schema_obj.pop("allOf")
            schema_obj.update(resolved_properties)

        # Recursively resolve properties for nested schema objects
        for key, value in schema_obj.items():
            schema_obj[key] = _resolve_complex_schema(value)
    elif isinstance(schema_obj, list):
        schema_obj = [_resolve_complex_schema(item) for item in schema_obj]

    return schema_obj
