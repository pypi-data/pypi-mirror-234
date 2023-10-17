import pathlib
import shutil

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

    # sample files don't matter when creating from a specification
    hub.tool.path.delete(
        root_directory / ctx.clean_name / "exec" / ctx.service_name / "sample.py"
    )
    hub.tool.path.delete(
        root_directory / ctx.clean_name / "states" / ctx.service_name / "sample.py"
    )
    hub.tool.path.delete(
        root_directory / "docs" / "ref" / "exec" / ctx.service_name / "sample.rst"
    )
    hub.tool.path.delete(
        root_directory / "docs" / "ref" / "states" / ctx.service_name / "sample.rst"
    )
    hub.tool.path.delete(
        root_directory
        / ctx.clean_name
        / "autogen"
        / ctx.service_name
        / "templates"
        / "sample.jinja2"
    )

    if ctx.get("templates_dir", None):
        # overwrite all files in target template with source template directory
        target = (
            root_directory / ctx.clean_name / "autogen" / ctx.service_name / "templates"
        )
        # Any existing file will be overwritten
        shutil.copytree(ctx.get("templates_dir"), target, dirs_exist_ok=True)
