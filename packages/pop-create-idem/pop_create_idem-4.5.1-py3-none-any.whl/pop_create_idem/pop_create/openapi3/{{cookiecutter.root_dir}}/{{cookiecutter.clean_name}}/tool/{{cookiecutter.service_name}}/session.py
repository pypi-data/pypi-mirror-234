import json
from typing import Any
from typing import Dict

import aiohttp


async def request(
        hub,
        ctx,
        method: str,
        path: str,
        query_params: Dict[str, str] = {},
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
):
    # Enable trace logging listener for the http client
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(hub.tool.{{cookiecutter.service_name}}.session.on_request_start)
    trace_config.on_request_end.append(hub.tool.{{cookiecutter.service_name}}.session.on_request_end)

    # path usually starts with "/" in openapi spec
    url = "".join((ctx.acct.endpoint_url.rstrip("/"), path))

    async with aiohttp.ClientSession(
        loop=hub.pop.Loop, trace_configs=[trace_config],
    ) as session:
        result = dict(ret=None, result=True, status=200, comment=[], headers={})

        if not headers.get("content-type"):
            headers["content-type"] = "application/json"
            headers["accept"] = "application/json"

        if "headers" in ctx.acct:
            # The acct login could set authorization and other headers
            headers.update(ctx.acct.headers)

        query_params_sanitized = {k: v for k, v in query_params.items() if v is not None}
        async with session.request(
            url=url,
            method=method.lower(),
            ssl=False,
            allow_redirects=True,
            params=query_params_sanitized,
            data=json.dumps(data),
            headers=headers,
        ) as response:
            result["status"] = response.status
            result["result"] = 200 <= response.status <= 204
            result["comment"].append(response.reason)
            result["headers"].update(response.headers)
            try:
                result["ret"] = hub.tool.type.dict.namespaced(await response.json())
                response.raise_for_status()
            except Exception as err:
                result["comment"].append(result["ret"])
                result["comment"].append(f"{err.__class__.__name__}: {err}")
                result["result"] = False
                if response.status != 404:
                    try:
                        ret = await response.read()
                        result["ret"] = ret.decode() if hasattr(ret, "decode") else ret
                    except Exception as ex_read_err:
                        result["comment"].append(
                            f"Failed to read response: {ex_read_err.__class__.__name__}: {ex_read_err}")

            return result


async def on_request_start(hub, session, trace_config_ctx, params):
    hub.log.debug("Starting %s" % params)


async def on_request_end(hub, session, trace_config_ctx, params):
    hub.log.debug("Ending %s" % params)
