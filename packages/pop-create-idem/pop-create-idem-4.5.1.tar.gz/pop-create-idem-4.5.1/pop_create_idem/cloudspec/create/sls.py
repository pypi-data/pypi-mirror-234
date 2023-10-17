import pathlib

from cloudspec import CloudSpec


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)

    for ref, plugin in cloud_spec.plugins.items():
        for function_name in ["present", "absent"]:
            func_data = plugin.functions.get(function_name)

            if func_data is None:
                continue

            path = root_directory / "example" / function_name
            sls_file = hub.cloudspec.parse.plugin.touch(
                root=path, ref=ref, is_test=False, is_sls=True
            )
            hub.tool.path.touch(sls_file)
            example_request_syntax_output = (
                hub.cloudspec.parse.example.state_request_syntax(
                    resource_name=ref,
                    ref=hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin),
                    func_name=function_name,
                    params=func_data.params,
                )
            )

            sls_file.write_text(example_request_syntax_output)
