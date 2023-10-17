"""
Functions for processing plugins
"""
import pathlib

from cloudspec import CloudSpecPlugin


def header(hub, plugin: CloudSpecPlugin, resource_header: str) -> str:
    """
    Initialize the render of a plugin file and return the template
    """
    # noinspection JinjaAutoinspect
    template = hub.tool.jinja.template(hub.cloudspec.template.plugin.HEADER)

    return template.render(plugin=plugin, resource_header=resource_header)


def ref(hub, ctx, ref: str) -> str:
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]
    return ".".join([ctx.service_name] + subs + [mod])


def resource_ref(hub, ctx, ref: str) -> str:
    split = ref.split(".")
    subs = split[1:] if ctx.service_name == split[0] else split
    return hub.tool.format.case.snake_to_title("_".join(subs))


def mod_ref(hub, ctx, ref: str, plugin: CloudSpecPlugin) -> str:
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]
    return ".".join([ctx.service_name] + subs + [plugin.virtualname or mod])


def touch(
    hub, root: pathlib.Path, ref: str, is_test: bool = False, is_sls: bool = False
):
    """
    Create all the files underneath the new sub
    """
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]

    if is_test:
        mod = f"test_{mod}"

    for sub in subs:
        root = root / sub

    if is_sls:
        root = root / f"{mod}.sls"
    else:
        root = root / f"{mod}.py"
    hub.tool.path.touch(root)
    return root
