import json
import pathlib
import timeit
from typing import List

from cloudspec import CloudSpec


def __init__(hub):
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    hub.pop.sub.load_subdirs(hub.cloudspec, recurse=True)


def cli(hub):
    """
    Validate json from the cli
    """
    hub.pop.sub.add(dyne_name="output")
    hub.pop.config.load(["cloudspec", "rend", "pop_create"], cli="cloudspec")

    with open(hub.OPT.cloudspec.input_file, "w+") as fh:
        data = json.load(fh)

    if hub.SUBPARSER == "validate":
        validated_spec = CloudSpec(**data)
        hub.output[hub.OPT.rend.output].display(dict(validated_spec))
    elif hub.SUBPARSER == "create":
        root_directory = pathlib.Path(hub.OPT.pop_create.directory)
        ctx = hub.pop_create.idem_cloud.init.context(
            hub.pop_create.init.context(), root_directory
        )
        ctx.cloud_spec = data
        hub.cloudspec.init.run(ctx, root_directory, hub.OPT.cloudspec.create_plugins)
    else:
        hub.log.error(f"Unknown subparser: {hub.SUBPARSER}")


def run(
    hub,
    ctx,
    root_directory: pathlib.Path,
    create_plugins: List[str],
):
    start_time = timeit.default_timer()

    cloud_spec_customize_plugin = ctx.get("cloud_spec_customize_plugin")
    if cloud_spec_customize_plugin:
        for customize_plugin in cloud_spec_customize_plugin:
            if customize_plugin not in hub.cloudspec.customize._loaded:
                print(
                    f"The cloud spec customize plugin '{customize_plugin}' is not loaded."
                )
                continue
            hub.cloudspec.init.run_customize_cloud_spec(ctx, customize_plugin)
    else:
        # Run through all loaded customization. This can support multiple abstracted customization plugins (e.g.
        # state, exec, test etc.) in a generated idem plugin
        for customize_plugin in hub.cloudspec.customize._loaded:
            hub.cloudspec.init.run_customize_cloud_spec(ctx, customize_plugin)

    ctx.cloud_spec = CloudSpec(**ctx.cloud_spec)

    for create_plugin in create_plugins:
        try:
            hub.log.info(f"Running create plugin: {create_plugin}")
            hub.cloudspec.create[create_plugin].run(ctx, root_directory)
        except Exception as e:
            hub.log.error(f"Failed to run create plugin: {create_plugin}")
            hub.log.error(e)
    print(
        f"Total time in creating plugins: {timeit.default_timer() - start_time} seconds"
    )


def run_customize_cloud_spec(hub, ctx, cloud_spec_customize_plugin):
    try:
        hub.log.debug(
            f"Running customization with plugin: {cloud_spec_customize_plugin}"
        )
        hub.cloudspec.customize[cloud_spec_customize_plugin].run(ctx)
        hub.log.debug(
            f"Updated cloud spec after customization with plugin '{cloud_spec_customize_plugin}': {json.dumps(ctx.cloud_spec, indent=4)}"
        )
    except Exception as customization_err:
        hub.log.error(
            f"Failed to customize using {cloud_spec_customize_plugin}: {customization_err}"
        )
