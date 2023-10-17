import copy
import os
import pathlib

import tqdm

HEADER_TEMPLATE = "States module for managing {}."


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = copy.deepcopy(ctx.cloud_spec)
    states_dir = root_directory / ctx.clean_name / "states" / ctx.service_name
    template_dir = (
        root_directory
        / ctx.clean_name
        / "autogen"
        / ctx.service_name
        / "templates"
        / "state"
    )

    for ref, plugin in tqdm.tqdm(
        cloud_spec.plugins.items(), desc=f"Generating state modules functions"
    ):
        mod_file = hub.cloudspec.parse.plugin.touch(states_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        state_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)
        resource_ref = hub.cloudspec.parse.plugin.resource_ref(ctx, ref)
        resource_header = HEADER_TEMPLATE.format(
            hub.tool.format.inflect.ENGINE.plural_noun(resource_ref)
        )

        plugin["contracts"] = ["resource"]

        to_write = hub.cloudspec.parse.plugin.header(
            plugin=plugin, resource_header=resource_header
        )
        if not plugin.functions:
            mod_file.write_text(to_write)
            continue
        func_data = hub.cloudspec.parse.function.parse(
            plugin.functions, targets=("present", "absent", "describe")
        )

        present_parameter = {}
        if func_data.get("present"):
            present_parameter = hub.cloudspec.parse.param.simple_map(
                plugin.functions["present"].params
            )

        common_params = {}
        if func_data.get("absent") and func_data.get("describe"):
            for name, param in plugin.functions["absent"].params.items():
                if name in plugin.functions["describe"].params:
                    common_params[name] = plugin.functions["describe"].params[name]

            common_params = hub.cloudspec.parse.param.mappings(common_params)

        # Create the present, absent, and describe functions; these are required for every state module
        for function_name, TEMPLATE in zip(
            ("present", "absent", "describe"),
            (
                hub.cloudspec.template.state.PRESENT_FUNCTION,
                hub.cloudspec.template.state.ABSENT_FUNCTION,
                hub.cloudspec.template.state.DESCRIBE_FUNCTION,
            ),
        ):
            if func_data.get(function_name):
                request_format_template_file = f"{template_dir}/{function_name}.jinja2"
                if os.path.isfile(request_format_template_file):
                    with open(f"{template_dir}/{function_name}.jinja2", "rb+") as f:
                        request_format = f.read().decode()
                else:
                    request_format = cloud_spec.request_format.get(function_name)

                template = hub.tool.jinja.template(
                    f"{TEMPLATE}\n    {request_format}\n\n\n"
                )

                example_request_syntax = None
                if function_name in ["present", "absent"]:
                    example_request_syntax = (
                        hub.cloudspec.parse.example.state_request_syntax(
                            resource_name=ref,
                            ref=hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin),
                            func_name=function_name,
                            params=plugin.functions.get(function_name).params,
                        )
                    )

                try:
                    to_write += template.render(
                        service_name=cloud_spec.service_name,
                        function=dict(
                            ref=ref,
                            state_ref=f"states.{state_ref}",
                            **func_data[function_name]["function"],
                            example_request_syntax=example_request_syntax,
                        ),
                        parameter=func_data[function_name]["parameter"],
                        present_parameter=present_parameter,
                        get_params=common_params,
                    )
                except Exception as err:
                    hub.log.error(
                        f"Failed to generate resource {resource_ref} function's action definitions for {function_name}: {err.__class__.__name__}: {err}"
                    )

                mod_file.write_text(to_write)
