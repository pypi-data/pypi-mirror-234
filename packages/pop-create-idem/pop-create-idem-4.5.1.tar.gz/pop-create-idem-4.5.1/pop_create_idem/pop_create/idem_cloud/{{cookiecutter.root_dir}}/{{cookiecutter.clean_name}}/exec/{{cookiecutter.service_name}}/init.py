def __init__(hub):
    hub.exec.{{cookiecutter.service_name}}.ENDPOINT_URLS = {{cookiecutter.servers}}
    # The default is the first in the list
    hub.exec.{{cookiecutter.service_name}}.DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"

    # This enables acct profiles that begin with "{{cookiecutter.acct_plugin}}" for {{cookiecutter.service_name}} modules
    hub.exec.{{cookiecutter.service_name}}.ACCT = ["{{cookiecutter.acct_plugin}}"]
