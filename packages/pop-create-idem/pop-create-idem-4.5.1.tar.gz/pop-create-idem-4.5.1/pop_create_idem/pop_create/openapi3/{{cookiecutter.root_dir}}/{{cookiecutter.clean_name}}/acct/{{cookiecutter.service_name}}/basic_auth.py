import base64

from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict

DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"


async def gather(hub, profiles) -> Dict[str, Any]:
    """
    Generate token with basic auth

    Example:
    .. code-block:: yaml

        {{cookiecutter.service_name}}:
          profile_name:
            username: my_user
            password: my_token
            endpoint_url: https://{{cookiecutter.service_name}}.com
    """
    sub_profiles = {}
    for (
            profile,
            ctx,
    ) in profiles.get("{{cookiecutter.service_name}}", {}).items():
        endpoint_url = ctx.get("endpoint_url")

        creds = f"{ctx.get('username')}:{ctx.get('password')}"
        temp_ctx = NamespaceDict(acct={
            "endpoint_url": endpoint_url,
            "headers": {
                "Authorization": f"Basic {base64.b64encode(creds.encode('utf-8')).decode('ascii')}"
            }
        })

        ret = await hub.tool.{{cookiecutter.service_name}}.session.request(
            temp_ctx,
            method="post",
            # TODO: Change Login path
            path="TODO".format(**{}),
            data={},
        )

        if not ret["result"]:
            error = f"Unable to authenticate: {ret.get('comment', '')}"
            hub.log.error(error)
            raise ConnectionError(error)

        # TODO: Find the token value in response
        access_token = ret["ret"][
            "token"
        ]
        sub_profiles[profile] = dict(
            endpoint_url=endpoint_url,
            # TODO: Replace the header that should be passed to future requests
            headers={"Authorization": f"Bearer {access_token}"},
        )
    return sub_profiles
