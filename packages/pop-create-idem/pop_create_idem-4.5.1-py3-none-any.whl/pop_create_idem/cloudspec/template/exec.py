FUNCTION = """
async def {{function.name}}(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}

        .. code-block:: python

            async def my_func(hub, ctx):
                ret = await hub.exec.{{ function.ref }}.{{ function.name }}(ctx, {{ function.required_call_params }})
                assert ret.result is True, ret.ref + ": " + ret.comment
                return ret.ret
    '''
"""
