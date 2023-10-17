import copy
import os.path
import pathlib

import tqdm


HEADER_TEMPLATE = "Exec module for managing {}."


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = copy.deepcopy(ctx.cloud_spec)
    exec_dir = root_directory / ctx.clean_name / "exec" / ctx.service_name
    template_dir = (
        root_directory
        / ctx.clean_name
        / "autogen"
        / ctx.service_name
        / "templates"
        / "exec"
    )

    for ref, plugin in tqdm.tqdm(
        cloud_spec.plugins.items(), desc=f"Generating exec functions"
    ):
        mod_file = hub.cloudspec.parse.plugin.touch(exec_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        resource_ref = hub.cloudspec.parse.plugin.resource_ref(ctx, ref)
        resource_header = HEADER_TEMPLATE.format(
            hub.tool.format.inflect.ENGINE.plural_noun(resource_ref)
        )

        plugin["func_alias"] = {"list_": "list"}
        if not plugin.get("contracts"):
            # plugin["contracts"] = ["auto_state", "soft_fail"]
            # At the moment, we do not fully support auto_state
            plugin["contracts"] = ["soft_fail"]

        exec_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)

        # Set up the base template
        if not plugin.functions:
            to_write = hub.cloudspec.parse.plugin.header(
                plugin=plugin, resource_header=resource_header
            )

        else:
            to_write = hub.cloudspec.parse.plugin.header(
                plugin=plugin, resource_header=resource_header
            )
            mod_file.write_text(to_write)
            func_data = hub.cloudspec.parse.function.parse(
                plugin.functions, targets=("get", "list", "create", "update", "delete")
            )

            present_parameter = {}
            if plugin.functions.get("create"):
                present_parameter = hub.cloudspec.parse.param.simple_map(
                    plugin.functions["create"].params
                )

            # Make the get, list, create, delete, and update functions; these are required for every auto_state exec module
            for function_name in ["get", "list", "create", "update", "delete"]:
                if func_data.get(function_name):
                    base_template = hub.cloudspec.template.auto_state[
                        function_name.upper()
                    ]

                    request_format_template_file = (
                        f"{template_dir}/{function_name}.jinja2"
                    )
                    if os.path.isfile(request_format_template_file):
                        with open(f"{template_dir}/{function_name}.jinja2", "rb+") as f:
                            request_format = f.read().decode()
                    else:
                        request_format = cloud_spec.request_format.get(function_name)

                    template_str = f"{base_template}\n    {request_format}\n\n\n"
                    template = hub.tool.jinja.template(template_str)

                    try:
                        to_write += template.render(
                            service_name=cloud_spec.service_name,
                            function=dict(
                                ref=ref,
                                exec_ref=f"exec.{exec_ref}",
                                **func_data[function_name]["function"],
                            ),
                            parameter=func_data[function_name]["parameter"],
                            present_parameter=present_parameter,
                        )
                    except Exception as err:
                        hub.log.error(
                            f"Failed to generate resource {resource_ref} function's action definitions for {function_name}: {err.__class__.__name__}: {err}"
                        )

        mod_file.write_text(to_write)
