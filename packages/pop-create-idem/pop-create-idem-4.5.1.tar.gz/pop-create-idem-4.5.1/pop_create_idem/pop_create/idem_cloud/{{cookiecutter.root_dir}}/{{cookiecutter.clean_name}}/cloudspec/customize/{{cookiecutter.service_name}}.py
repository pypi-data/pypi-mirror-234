def run(hub, ctx):
    """
    Use this plugin to customize cloud spec

    ctx.cloud_spec(NamespaceDict):
        The generated cloud_spec from a source in the following format:

        {
            "project_name": "",
            "service_name": "",
            "api_version": "latest",
            "request_format": "",
            "plugins": {
                plugin_name: {
                    "imports": [],
                    "virtual_imports": [],
                    "func_alias": {},
                    "virtualname": "",
                    "doc": "docstring",
                    "functions": {
                        "function_name": {
                            "doc": "",
                            "return_type": "",
                            "hardcoded": {},
                            "params": {
                                "param_name": {
                                    "doc": "Docstring for this parameter",
                                    "param_type": "Type",
                                    "required": True|False,
                                    "default": "",
                                    "target": "",
                                    "target_type": "mapping|value|arg|kwargs"
                                    "member": {
                                        "name": "param_type_name",
                                        "params": {
                                            "nested_param1_name": CloudSpecParam,
                                            "nested_param2_name": CloudSpecParam,
                                            ...
                                        }
                                    },
                                },
                            }
                        },
                    }
                },
            }
        }
    """
    # TODO: Replace with custom logic
    pass
