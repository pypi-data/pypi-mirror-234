CLI_CONFIG = {
    "create_plugin": {"subcommands": ["_global_"], "dyne": "pop_create"},
    "simple_service_name": {
        "options": ["--cloud", "--cloud-name"],
        "subcommands": ["_global_"],
        "dyne": "pop_create",
    },
    "acct_plugin": {
        "subcommands": ["idem-cloud", "openapi3", "swagger"],
        "dyne": "pop_create",
    },
    "target": {
        "subcommands": ["openapi3", "swagger"],
        "nargs": "+",
        "dyne": "pop_create",
    },
    "specification": {
        "options": ["--spec", "--file", "--url"],
        "nargs": "+",
        "subcommands": ["openapi3", "swagger", "idem-cloud"],
        "dyne": "pop_create",
    },
    "templates_dir": {
        "options": ["--td"],
        "subcommands": ["_global_"],
        "dyne": "pop_create",
    },
    "cloud_spec_customize_plugin": {
        "options": ["--customize-plugin"],
        "nargs": "+",
        "subcommands": ["openapi3", "swagger", "idem-cloud"],
        "dyne": "pop_create",
    },
}
CONFIG = {
    "create_plugin": {
        "default": "state_modules",
        "dyne": "pop_create",
        "help": "The `create` plugin to use for resource modules. The other options are 'auto_states', "
        "'exec_modules', 'sls', and 'templates'.",
    },
    "acct_plugin": {
        "default": None,
        "help": "The acct plugin to use for authentication -- default is to create a new plugin",
        "dyne": "pop_create",
    },
    "target": {
        "default": None,
        "help": "Target service resource path. This is useful when generating Idem plugin only for a subset of service resources",
        "dyne": "pop_create",
    },
    "simple_service_name": {
        "default": None,
        "help": "Short name of the cloud being bootstrapped",
        "dyne": "pop_create",
    },
    "specification": {
        "default": None,
        "help": "The url or file path to a spec",
        "dyne": "pop_create",
    },
    "templates_dir": {
        "default": None,
        "help": "The full absolute path of directory where jinja templates are saved",
        "dyne": "pop_create",
    },
    "cloud_spec_customize_plugin": {
        "default": None,
        "help": "The name of the plugins for customizing cloud spec before resource modules are created. The default "
        "customize plugin can be found under 'root_dir > project_name > cloudspec > customize`",
        "dyne": "pop_create",
    },
}
SUBCOMMANDS = {
    # https://openapi.tools/#converters
    "idem-cloud": {"help": "Boostrap an idem cloud project", "dyne": "pop_create"},
    "openapi3": {
        "help": "Create idem_cloud modules based off of an openapi3 spec",
        "dyne": "pop_create",
    },
    "swagger": {
        "help": "Create idem_cloud modules based off of a swagger spec",
        "dyne": "pop_create",
    },
}
DYNE = {
    "pop_create": ["pop_create"],
    "cloudspec": ["cloudspec"],
    "tool": ["tool"],
    "jinja": ["jinja"],
}
