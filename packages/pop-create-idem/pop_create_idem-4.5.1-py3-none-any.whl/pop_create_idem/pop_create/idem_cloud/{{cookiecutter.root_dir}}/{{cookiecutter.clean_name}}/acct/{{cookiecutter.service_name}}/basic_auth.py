import base64

DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"


async def gather(hub):
    """
    Authenticate with a username and password to the given endpoint url.
    Any extra parameters will be saved as part of the profile.

    Example:

    .. code-block:: sls

        {{cookiecutter.service_name}}:
          profile_name:
            username: my_user
            password: my_token
            endpoint_url: https://{{cookiecutter.service_name}}.com
    """
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get(
        "{{cookiecutter.service_name}}.basic_auth", {}
    ).items():
        creds = f"{ctx.pop('username')}:{ctx.pop('password')}"
        sub_profiles[profile] = dict(
            endpoint_url=ctx.pop("endpoint_url"),
            headers={
                "Authorization": f"Basic {base64.b64encode(creds.encode('utf-8')).decode('ascii')}"
            },
            **ctx
        )

    return sub_profiles
