import json
import pathlib

from dict_tools.data import NamespaceDict


def __init__(hub):
    hub.pop.sub.add(dyne_name="cloudspec")


def context(hub, ctx, directory: pathlib.Path):
    # all template files are copied without render
    ctx["_copy_without_render"] = ["*.jinja2"]

    if hub.OPT.pop_create.cloud_spec_customize_plugin:
        ctx[
            "cloud_spec_customize_plugin"
        ] = hub.OPT.pop_create.cloud_spec_customize_plugin

    # non openapi/swagger based would not have cloud_spec here
    if "cloud_spec" not in ctx or not ctx.cloud_spec:
        # If an acct plugin was passed in then we don't need to create auth plugins
        if ctx.get("simple_service_name"):
            ctx.service_name = ctx.simple_service_name
        elif not ctx.get("service_name"):
            ctx.service_name = (
                ctx.clean_name.replace("idem", "").replace("cloud", "").strip("_")
            )

        ctx.clean_api_version = ctx.get("clean_api_version")
        ctx.cloud_api_version = ctx.get("cloud_api_version")
        ctx.servers = ctx.get("servers", [""])
        if ctx.specification:
            with open(ctx.specification, "w+") as fh:
                data = json.load(fh)

            ctx.cloud_spec = data
        else:
            ctx.cloud_spec = NamespaceDict(
                api_version=ctx.get("cloud_api_version"),
                project_name=ctx.project_name,
                service_name=ctx.service_name,
                request_format=None,
                plugins={},
            )

        ctx.has_acct_plugin = bool(ctx.acct_plugin)
        if not ctx.has_acct_plugin:
            # Create auth plugins
            ctx.acct_plugin = ctx.service_name

    # sphynx docs generation related settings
    ctx["docs_modindex_common_prefix"] = [
        f"{ctx['clean_name']}.states.{ctx['service_name']}",
        f"{ctx['clean_name']}.exec.{ctx['service_name']}",
    ]
    ctx["docs_autogen_config"] = ["exec/", "states/"]

    return ctx
