import os
import pathlib

from cloudspec import CloudSpec

HEADER_TEMPLATE = "Exec module for managing {}."


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)
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
        cli_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)
        resource_ref = hub.cloudspec.parse.plugin.resource_ref(ctx, ref)
        resource_header = HEADER_TEMPLATE.format(
            hub.tool.format.inflect.ENGINE.plural_noun(resource_ref)
        )

        plugin["func_alias"] = {"list_": "list"}

        to_write = hub.cloudspec.parse.plugin.header(
            plugin=plugin, resource_header=resource_header
        )

        for function_name, function_data in plugin.functions.items():
            if function_name in ["present", "absent", "describe"]:
                # If plugin comes in with all methods, let's not create for state_modules functions
                continue

            request_format_template_file = f"{template_dir}/{function_name}.jinja2"
            if os.path.isfile(request_format_template_file):
                with open(f"{template_dir}/{function_name}.jinja2", "rb+") as f:
                    request_format = f.read().decode()
            else:
                request_format = cloud_spec.request_format.get(function_name)

            template = hub.tool.jinja.template(
                f"{hub.cloudspec.template.exec.FUNCTION}\n    {request_format}\n\n\n"
            )

            function_alias = plugin.func_alias.get(function_name, function_name)

            try:
                to_write += template.render(
                    function=dict(
                        name=function_name,
                        hardcoded=function_data.hardcoded,
                        doc=hub.cloudspec.parse.function.doc(function_data)
                        + hub.cloudspec.parse.param.sphinx_docs(function_data.params)
                        + hub.cloudspec.parse.function.return_type(function_data),
                        ref=f"{ref}.{function_alias}",
                        cli_ref=f"{cli_ref}.{function_alias}",
                        header_params=hub.cloudspec.parse.param.headers(
                            function_data.params
                        ),
                        required_call_params=hub.cloudspec.parse.param.required_call_params(
                            function_data.params
                        ),
                        return_type=function_data.return_type,
                    ),
                    parameter=dict(
                        mapping=hub.cloudspec.parse.param.mappings(function_data.params)
                    ),
                )
            except Exception as err:
                hub.log.error(
                    f"Failed to generate resource {resource_ref} function's action definitions for {function_name}: {err.__class__.__name__}: {err}"
                )

        mod_file.write_text(to_write)
