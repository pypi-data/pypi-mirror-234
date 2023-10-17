from typing import Any
from typing import Dict
import base64

from dict_tools.data import NamespaceDict

DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"

async def gather(hub, profiles) -> Dict[str, Any]:
    """
    Authenticate with client_credentials

    Example:
    .. code-block:: yaml

        {{cookiecutter.service_name}}:
          profile_name:
            client_id: <client-id>
            client_secret: <client-secret>
            tenant: <tenant-id>
            api_version: <version-info>
            endpoint_url: {{cookiecutter.servers|join('|')}}
    """
    sub_profiles = {}
    for (
        profile,
        ctx,
    ) in profiles.get("{{cookiecutter.service_name}}", {}).items():
        client_id = ctx.get("client_id")
        client_secret = ctx.get("client_secret")
        org_id = ctx.get("org_id")

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
                # TODO: Change based on login api request data
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "org_id": org_id,
            },
            headers={
                # TODO: Change based on login api request data
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('ascii')}"
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
