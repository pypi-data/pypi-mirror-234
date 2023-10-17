from typing import Any
from typing import Dict

import openapi3.object_base
import tqdm


def plugins(hub, ctx, api: openapi3.OpenAPI) -> Dict[str, Any]:
    ret = {}
    paths: openapi3.object_base.Map = api.paths

    all_schemas = hub.pop_create.openapi3.schemas.parse(api)

    for name, path in tqdm.tqdm(paths.items(), desc="Parsing paths"):
        if ctx.target and name not in ctx.target:
            continue
        if not isinstance(path, openapi3.paths.Path):
            # Let's not fail but continue to other paths instead
            hub.log.warning(
                f"The {name} is not an instance of Path. It will not be parsed."
            )
            continue

        # Get the request type that works for this request
        for request_type in path.raw_element.keys():
            func: openapi3.paths.Operation = getattr(path, request_type, None)
            if not func:
                continue

            plugin = None
            refs = None
            if func.tags:
                subs = [hub.tool.format.case.snake(sub) for sub in func.tags]
                if not subs:
                    plugin = "init"
                else:
                    plugin = subs.pop()

                refs = subs + [plugin]
            elif func.get_path():
                # e.g. "/pets", /pets/{id} -> "pets" become plugin
                # func.get_path() could look like this "paths./pets/{id}.get
                # second element is always the actual path itself
                func_path = func.get_path().split(".")[1]
                plugin = func_path.lstrip("/").split("/")[0]
                refs = [hub.tool.format.case.snake(plugin)]

            if not plugin:
                hub.log.warning(
                    f"Not sure how to find plugin for {name}. Try using 'tags'"
                )
                continue

            plugin = hub.tool.format.case.snake(plugin)

            # service name is already added in pop-create
            ref = ".".join(refs)
            if ref not in ret:
                # This is the first time we have looked at this plugin
                ret[ref] = {
                    "functions": {},
                    "doc": "",
                    "imports": [
                        "from typing import Any",
                        "from typing import Dict",
                        "from typing import List",
                        "from collections import OrderedDict",
                        "from dataclasses import field",
                        "from dataclasses import make_dataclass",
                        "import dict_tools.differ as differ",
                    ],
                }

            # See if this function will be reserved CRUD operations, if so change the name
            reserved_func_name = (
                hub.pop_create.openapi3.parse.resolve_reserved_function_name(
                    name, plugin, request_type, func
                )
            )

            # Anything that doesn't resolved in reserved function name, would go into tools/{resource_name}/*
            func_name = (
                hub.pop_create.openapi3.parse.resolve_function_name(
                    name, plugin, request_type, func
                )
                if not reserved_func_name
                else reserved_func_name
            )

            try:
                ret[ref]["functions"][
                    func_name
                ] = hub.pop_create.openapi3.function.parse(
                    ctx,
                    request_type,
                    name,
                    plugin,
                    func,
                    all_schemas,
                )
            except Exception as e:
                hub.log.debug(
                    f"Failed to parse function data for {plugin}: {request_type} '{name}': {e.__class__.__name__}: {e}"
                )

    for ref, plugin in ret.items():
        # For each 'ref' aka resource, exec.list of a resource will most likely return same type of response as that of
        # exec.get just in list
        if "get" in plugin["functions"] and "list" in plugin["functions"]:
            if "hardcoded" not in plugin["functions"]["list"]:
                # just a safeguard. It is most likely be present.
                plugin["functions"]["list"]["hardcoded"] = {}
            plugin["functions"]["list"]["hardcoded"]["response_mappings"] = (
                plugin["functions"]["get"]
                .get("hardcoded", {})
                .get("response_mappings", {})
            )
        # This happens when API uses PUT/PATCH for both create and update operations
        if "update" in plugin["functions"] and "create" not in plugin["functions"]:
            hub.log.debug(
                f"Copy 'update' function to 'create' function for plugin ref {ref}"
            )
            plugin["functions"]["create"] = plugin["functions"]["update"]

    return ret


def resolve_reserved_function_name(
    hub, name: str, plugin: str, request_type: str, func: openapi3.paths.Operation
):
    # Do not make deprecated API paths into CRUDs and throw them into tools/*
    possible_resource_names = tuple(
        [
            # e.g. /store_order, /store-order, /store_orders, /store-orders
            plugin,
            plugin.replace("_", "-"),
            f"{plugin}s",
            f"{plugin.replace('_', '-')}s",
        ]
    )
    if not func.deprecated:
        # e.g. plugin: pets, path: /pets
        if name.endswith(possible_resource_names):
            # list/post
            if request_type == "get":
                return "list"
            elif request_type == "post":
                return "create"
            elif request_type == "put":
                # PUT /pets
                return "update"
        # e.g.: plugin: pets, path: /pets/{id}
        elif name.rsplit("/", 1)[0].endswith(possible_resource_names):
            # get/list/put
            if request_type == "get":
                return "get"
            elif request_type == "put" or request_type == "patch":
                return "update"
            elif request_type == "delete":
                return "delete"

    return None


def resolve_function_name(
    hub, name: str, plugin: str, request_type: str, func: openapi3.paths.Operation
):
    # This is the preferred way to get a function name
    # However, some APIs can just put reserved/known operationId which is not helpful here in parsing and codegen
    # Also, we always handle reserved/known operation names in different way
    func_name = (
        func.operationId
        if func.operationId
        not in ["get", "list", "create", "patch", "update", "put", "delete"]
        else None
    )

    # Fallback function name based on the pets example
    if not func_name and " " in name:
        func_name = "_".join(name.split(" ")[1:]).lower()

    if not func_name and func.summary:
        # Truncate it to 10 characters and add plugin name in the end
        func_name = f"{func.summary[:10]}_{plugin}"

    if not func_name and request_type:
        # No operationId, no summary, let's create it with path
        # GET /pets/{id}/types -> get_pets_id_types
        func_name = (
            f"{request_type}_{name.replace('{', '').replace('}', '').replace('/', '_')}"
        )

    if not func_name and func.extensions:
        func_name = func.extensions[sorted(func.extensions.keys())[0]]

    # Maybe we need more fallbacks, you tell me
    if not func_name:
        # Maybe a fallback based on the path and method?
        raise AttributeError(f"Not sure how to find func name for {name}, help me out")

    return hub.tool.format.case.snake(func_name)
