"""Exec module for managing sample resources."""

# This will put our "list_" function on the hub as "list"
# Func alias works around function names that shadow builtin python names
__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str):
    """Get a sample resource via resource_id.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            An identifier of the resource in the provider.

    Returns:
        Dict[str, Any]:
            Returns sample resource in present format

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec {{cookiecutter.service_name}}.sample.get name=my_resource resource_id=resource_1

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: {{cookiecutter.service_name}}.sample.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_1
    """
    return dict(
        comment=["sample get"],
        ret={
            "name": name,
            "resource_id": resource_id,
            "description": "Sample description"
        },
        result=True)


async def list_(hub, ctx, name: str = None):
    """List sample resources.

    Args:
        name(str, Optional):
            The name of the Idem state.

    Returns:
        Dict[str, Any]:
            Returns sample resources in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec {{cookiecutter.service_name}}.sample.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: {{cookiecutter.service_name}}.sample.list
    """
    return dict(
        comment=["sample get"],
        ret=[{
            "name": name,
            "resource_id": "resource_1",
            "description": "Sample description"
        }],
        result=True)


async def create(hub, ctx, name: str, resource_id: str = None, description: str = None):
    """Create a sample resource.

    Args:
        name(str):
            The state name.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        description(str, Optional):
            Description of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]:
            Returns sample resource in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec {{cookiecutter.service_name}}.sample.create name=my_resource description="Managed by Idem"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: {{cookiecutter.service_name}}.sample.create
                - kwargs:
                    name: my_resource
                    description: Managed by Idem
    """
    return dict(
        comment=["sample create"],
        ret={
                "name": name,
                "resource_id": resource_id if resource_id else "resource_1",
                "description": description if description else "Sample description",
            },
        result=True)


async def update(hub, ctx, name: str, resource_id: str, description: str = None):
    """Update a sample resource.

    Args:
        name(str):
            The state name.

        resource_id(str):
            An identifier of the resource in the provider.

        description(str, Optional):
            Description of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]:
            Returns sample resource in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec {{cookiecutter.service_name}}.sample.update name=my_resource resource_id=resource_1 description="Managed by Idem"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: {{cookiecutter.service_name}}.sample.update
                - kwargs:
                    resource_id: resource_1
                    name: my_resource
                    description: Managed by Idem
    """
    return dict(
        comment=["sample update"],
        ret={
                "name": name,
                "resource_id": resource_id,
                "description": description if description else "Sample description"
            },
        result=True)


async def delete(hub, ctx, name: str, resource_id: str):
    """Delete a sample resource.

    Args:
        name(str):
            The state name.

        resource_id(str):
            An identifier of the resource in the provider.

    Returns:
        Dict[str, Any]:
            Returns success or failure

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec {{cookiecutter.service_name}}.sample.delete name=my_resource resource_id=resource_1

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: {{cookiecutter.service_name}}.sample.delete
                - kwargs:
                    resource_id: resource_1
                    name: my_resource
    """
    return dict(
        comment=["sample delete"],
        ret={},
        result=True)
