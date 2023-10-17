from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict

DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"

async def gather(hub, profiles) -> Dict[str, Any]:
    """
    Authenticate with api_key

    Example:
    .. code-block:: yaml

        {{cookiecutter.service_name}}:
          profile_name:
            api_version: <version-info>
            api_key: <api-key>
            endpoint_url: {{cookiecutter.servers|join('|')}}
    """
    sub_profiles = {}
    for (
        profile,
        ctx,
    ) in profiles.get("{{cookiecutter.service_name}}", {}).items():
        api_key = ctx.get("api_key")
        endpoint_url = ctx.get("endpoint_url")
        api_version = ctx.get("api_version")

        temp_ctx = NamespaceDict(acct={
            "endpoint_url": endpoint_url,
            "api_version": api_version,
        })

        ret = await hub.tool.{{cookiecutter.service_name}}.session.request(
            temp_ctx,
            method="post",
            # TODO: Change login path
            path="TODO".format(**{}),
            data={
                # TODO: pass api_key to respective
                "X-API-KEY": api_key,
                "refreshToken": api_key
            },
        )

        if not ret["result"]:
            error = f"Unable to authenticate: {ret.get('comment', '')}"
            hub.log.error(error)
            raise ConnectionError(error)

        access_token = ret["ret"][
            # TODO: Replace response key with corresponding API response
            "token"
        ]
        sub_profiles[profile] = dict(
            endpoint_url=endpoint_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
    return sub_profiles
