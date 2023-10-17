import copy
import os
import pathlib

import tqdm
from dict_tools.data import NamespaceDict

HEADER_TEMPLATE = "Utility functions for {}."


def run(hub, ctx, root_directory: pathlib.Path):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = copy.deepcopy(ctx.cloud_spec)
    tool_dir = root_directory / ctx.clean_name / "tool" / ctx.service_name
    template_dir = (
        root_directory
        / ctx.clean_name
        / "autogen"
        / ctx.service_name
        / "templates"
        / "tool"
    )

    for ref, plugin in tqdm.tqdm(
        cloud_spec.plugins.items(), desc=f"Generating tool functions"
    ):
        mod_file = hub.cloudspec.parse.plugin.touch(tool_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        module_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)
        resource_ref = hub.cloudspec.parse.plugin.resource_ref(ctx, ref)
        resource_header = HEADER_TEMPLATE.format(
            hub.tool.format.inflect.ENGINE.plural_noun(resource_ref)
        )

        # Set up the base template
        if not plugin.functions:
            to_write = hub.cloudspec.parse.plugin.header(
                plugin=plugin, resource_header=resource_header
            )
        else:
            to_write = hub.cloudspec.parse.plugin.header(
                plugin=plugin, resource_header=resource_header
            )

            tool_functions = NamespaceDict(
                filter(
                    # It is not a known function for Idem, and it is not a test function.
                    lambda item: item[0]
                    not in [
                        "get",
                        "list",
                        "create",
                        "update",
                        "delete",
                        "present",
                        "absent",
                        "describe",
                    ]
                    and "test_module_type" not in item[1].hardcoded,
                    plugin.functions.items(),
                )
            )
            for func_name, func_data in tool_functions.items():
                function_request_format_template_file = (
                    f"{template_dir}/{func_name}.jinja2"
                )
                default_request_format_template_file = f"{template_dir}/default.jinja2"
                if os.path.isfile(function_request_format_template_file):
                    with open(function_request_format_template_file, "rb+") as f:
                        request_format = f.read().decode()
                elif os.path.isfile(default_request_format_template_file):
                    with open(default_request_format_template_file, "rb+") as f:
                        request_format = f.read().decode()
                else:
                    # cloudspec was provided with hardcoded request format
                    request_format = cloud_spec.request_format.get(func_name)

                template = hub.tool.jinja.template(
                    f"{hub.cloudspec.template.tool.FUNCTION}\n    {request_format}\n\n"
                )

                doc = hub.cloudspec.parse.function.doc(func_data)
                doc += hub.cloudspec.parse.param.sphinx_docs(func_data.params)
                doc += "\n\n    Returns:\n        Dict[str, Any]\n"

                func_data["doc"] = doc

                try:
                    to_write += template.render(
                        function=dict(
                            name=func_name,
                            ref=ref,
                            module_ref=f"tool.{module_ref}",
                            **func_data,
                            header_params=hub.cloudspec.parse.param.headers(
                                func_data.params
                            ),
                        ),
                        parameter=dict(
                            mapping=hub.cloudspec.parse.param.mappings(func_data.params)
                        ),
                    )
                except Exception as err:
                    hub.log.error(
                        f"Failed to generate resource {resource_ref} function's action definitions for {func_name}: {err.__class__.__name__}: {err}"
                    )

        mod_file.write_text(to_write)
