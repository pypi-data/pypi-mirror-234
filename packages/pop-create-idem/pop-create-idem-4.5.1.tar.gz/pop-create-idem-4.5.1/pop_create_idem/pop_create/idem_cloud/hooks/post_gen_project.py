import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()

    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pop_create")
    hub.pop.sub.add(dyne_name="cloudspec")
    hub.pop.sub.add(dyne_name="config")
    hub.config.integrate.load(
        ["cloudspec", "pop_create"], "cloudspec", parse_cli=False, logs=False
    )
    ctx = NamespaceDict({{cookiecutter}})

    if ctx.create_plugin == "auto_states":
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=["auto_state", "tool", "tests", "docs"],
        )
    elif ctx.create_plugin == "exec_modules":
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=["exec_modules", "tool", "tests", "docs"],
        )
    elif ctx.create_plugin == "state_modules":
        # For now restrict only CRUDs for exec modules, auto_state already does that
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=[
                "auto_state",
                "tool",
                "state_modules",
                "tests",
                "sls",
                "docs",
            ],
        )
    elif ctx.create_plugin == "templates":
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=["templates"],
        )
    elif ctx.create_plugin == "test_modules":
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=["templates", "tests"],
        )
    elif ctx.create_plugin == "sls":
        hub.cloudspec.init.run(
            ctx,
            root_directory,
            create_plugins=["sls"],
        )
    else:
        raise ValueError(f"Invalid input '{ctx.create_plugin}' for --create-plugin.")

    # Sanitize based on other arguments
    if ctx.has_acct_plugin:
        hub.tool.path.rmtree(root_directory / ctx.clean_name / "acct")

    # End with the cicd template
    hub.pop_create.init.run(directory=root_directory, subparsers=["cicd"], **ctx)

    # TODO Run sphinx on the docstrings to make sure it all works
