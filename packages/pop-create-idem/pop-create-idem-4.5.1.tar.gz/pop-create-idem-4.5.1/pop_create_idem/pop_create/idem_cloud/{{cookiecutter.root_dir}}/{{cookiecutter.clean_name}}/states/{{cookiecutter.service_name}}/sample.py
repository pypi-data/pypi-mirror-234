"""State module for a sample state.

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide rst todos)
    A sample state using the sample idem_cloud modules for an idea of what a state module should look like.
    All states should have a "present", "absent" and "describe" functions, nothing else.
    Any additional functionality that needs to be exposed via Idem CLI, should be added to Exec module.
"""
from typing import Dict, Any
import dict_tools.differ as differ

__contracts__ = ["resource"]  # , "soft_fail"]

async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    description: str = None
) -> Dict[str, Any]:
    """Ensure that a resource exists and is in the correct state.

    Args:
        name(str):
            The state name.

        resource_id(str):
            An identifier of the resource in the provider. Defaults to None.

        description(str, Optional):
            Description of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

          my_state_name:
            {{cookiecutter.service_name}}.sample.present:
              - name: a_sample_name
              - description: Managed by Idem
    """
    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    if resource_id:
        before = await hub.exec.{{cookiecutter.service_name}}.sample.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(
            f"{{cookiecutter.service_name}}.sample: {name} already exists"
        )

        # If there are changes in desired state from existing state
        changes = differ.deep_diff(before.ret if before.ret else {}, desired_state)

        if bool(changes.get("new")):
            if ctx.test:
                # If `idem state` was run with the `--test` flag, then don't actually make any changes in the provider
                result["new_state"] = hub.tool.{{cookiecutter.service_name}}.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state=desired_state
                )
                result["comment"] = (
                    f"Would update {{cookiecutter.service_name}}.sample: {name}"
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.{{cookiecutter.service_name}}.sample.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    description=description,
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated '{{cookiecutter.service_name}}.sample: {name}'")
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.hub.tool.{{cookiecutter.service_name}}.generate_test_state(
                enforced_state={},
                desired_state=desired_state
            )
            result["comment"] = (
            f"Would create {{cookiecutter.service_name}}.sample: {name}",)
            return result
        else:
            create_ret = await hub.exec.{{cookiecutter.service_name}}.sample.create(
                ctx,
                name=name,
                description=description
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(
                    f"Created '{{cookiecutter.service_name}}.sample: {name}'")
                resource_id = create_ret["ret"]["resource_id"]
                # Safeguard for any future errors so that the resource_id is saved in the ESM
                result["new_state"] = dict(name=name, resource_id=resource_id)
            else:
                result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    after = await hub.exec.{{cookiecutter.service_name}}.sample.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    result["new_state"] = after.ret
    return result


async def absent(hub, ctx, name: str, resource_id: str = None):
    """Delete resource in the cloud provider

    Args:
        name(str):
            The state name.

        resource_id(str):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

          my_state_name:
            {{cookiecutter.service_name}}.sample.absent:
              - name: item_name
    """
    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(
            f"'{{cookiecutter.service_name}}.sample: {name}' already absent")
        return result

    before = await hub.exec.{{cookiecutter.service_name}}.sample.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"{{cookiecutter.service_name}}.sample: {name}"
            return result

        delete_ret = await hub.exec.{{cookiecutter.service_name}}.sample.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(
                f"Deleted {{cookiecutter.service_name}}.sample: {name}")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(
            f"{{cookiecutter.service_name}}.sample: {name} already absent")
        return result

    result["old_state"] = before.ret
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    Describes one or more sample states in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe {{cookiecutter.service_name}}.sample
    """
    result = {}

    ret = await hub.exec.{{cookiecutter.service_name}}.sample.list(
        ctx
    )

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe {{cookiecutter.service_name}}.sample {ret['comment']}")
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "{{cookiecutter.service_name}}.sample.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
