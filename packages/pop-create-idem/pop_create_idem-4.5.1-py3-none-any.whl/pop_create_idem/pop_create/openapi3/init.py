import os
import pathlib
from typing import Dict

import openapi3.object_base
import requests
import yaml
from dict_tools.data import NamespaceDict


def context(hub, ctx, directory: pathlib.Path):
    if ctx.get("simple_service_name"):
        ctx.service_name = ctx.simple_service_name
    elif not ctx.get("service_name"):
        ctx.service_name = (
            ctx.clean_name.replace("idem", "").replace("cloud", "").strip("_")
        )

    ctx.has_acct_plugin = bool(ctx.acct_plugin)
    if not ctx.has_acct_plugin:
        # Create auth plugins
        ctx.acct_plugin = ctx.service_name

    # Add extra templates provided by openapi3
    if not ctx.get("templates_dir"):
        # Use default templates
        ctx["templates_dir"] = (
            os.path.dirname(os.path.realpath(__file__))
            + "/{{cookiecutter.root_dir}}/{{cookiecutter.clean_name}}/autogen/{{cookiecutter.service_name}}/templates/"
        )

    # all template files are copied without render
    ctx["_copy_without_render"] = ["*.jinja2"]

    merged_plugins = {}
    for specification in ctx.specification:
        # Read the spec from URL or local file (Yaml)
        spec = hub.pop_create.openapi3.init.read(source=specification)
        api = openapi3.OpenAPI(spec, validate=True)
        errors = api.errors()
        if errors:
            for e in errors:
                hub.log.warning(e)

        # list these as defaults in the acct plugin
        if api.servers:
            ctx.servers = [x.url for x in api.servers]
        else:
            ctx.servers = ctx.get("servers", [""])

        hub.log.debug(f"Working with openapi spec version: {api.openapi}")

        ctx.cloud_api_version = api.info.version or "latest"
        ctx.clean_api_version = hub.tool.format.case.snake(ctx.cloud_api_version).strip(
            "_"
        )

        if not ctx.clean_api_version:
            ctx.clean_api_version = ctx.get("clean_api_version")

        if not ctx.cloud_api_version:
            ctx.cloud_api_version = ctx.get("cloud_api_version")

        # If the api version starts with a digit then make sure it can be used for python namespacing
        if ctx.clean_api_version[0].isdigit():
            ctx.clean_api_version = "v" + ctx.clean_api_version

        # Get function plugins
        plugins = hub.pop_create.openapi3.parse.plugins(ctx, api)

        # Add any missing function which is required for idem resource modules
        plugins = hub.pop_create.openapi3.init.add_missing_known_functions(ctx, plugins)

        # Add tests function
        plugins = hub.pop_create.openapi3.init.add_tests_functions(ctx, plugins)
        merged_plugins.update(plugins)

    ctx.cloud_spec = NamespaceDict(
        api_version=ctx.cloud_api_version,
        project_name=ctx.project_name,
        service_name=ctx.service_name,
        request_format={},
        plugins=merged_plugins,
    )

    hub.pop_create.init.run(directory=directory, subparsers=["idem_cloud"], **ctx)

    return ctx


def read(hub, source: str or Dict):
    """
    If the path is a file, then parse the json contents of the file,
    If the path is a url, then return a json response from the url.
    """
    if isinstance(source, Dict):
        return source

    path = pathlib.Path(source)

    if path.exists():
        with path.open("r") as fh:
            ret = yaml.safe_load(fh)
    else:
        request = requests.get(source, headers={"Content-Type": "application/json"})
        ret = request.json()

    return ret


def add_missing_known_functions(hub, ctx, plugins):
    # This is to make sure we still create standard skeletons for CRUD operations in exec
    # This way the only missing part would be API call in those modules
    for ref in list(plugins):
        for idem_func_name in ["get", "list", "create", "update", "delete"]:
            if not plugins[ref].get("functions", {}).get(idem_func_name):
                plugins[ref]["functions"][idem_func_name] = {
                    "doc": "",
                    "params": {},
                    "hardcoded": {
                        "method": "TODO",
                        "path": "TODO",
                        "service_name": ctx.service_name,
                        "resource_name": ref,
                    },
                }

    # Just add these state modules functions by default
    for ref in list(plugins):
        for func_name in list(plugins.get(ref).get("functions", {})):
            if func_name == "create":
                plugins[ref]["functions"]["present"] = (
                    plugins.get(ref).get("functions", {}).get(func_name)
                )
            elif func_name == "delete":
                plugins[ref]["functions"]["absent"] = (
                    plugins.get(ref).get("functions", {}).get(func_name)
                )
            elif func_name == "list":
                plugins[ref]["functions"]["describe"] = (
                    plugins.get(ref).get("functions", {}).get(func_name)
                )

    return plugins


def add_tests_functions(hub, ctx, plugins):
    for ref in list(plugins):
        functions = plugins[ref].get("functions", {}).copy()
        for func_name, func_data in functions.items():
            plugins[ref]["functions"][
                f"test_{func_name}"
            ] = hub.pop_create.openapi3.function.create_test_for_function(
                ctx=ctx, func_name=func_name, func_data=func_data
            )

    return plugins
