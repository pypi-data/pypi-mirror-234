CREATE = """
async def {{function.name}}(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              {{ function.ref }}.present:
                - {{ function.required_call_params.split(", ")|join("\n                - ")|replace("=", ": ") }}

        Exec call from the CLI:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}
    '''
"""

UPDATE = """
async def {{function.name}}(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              {{ function.ref }}.present:
                - {{ function.required_call_params.split(", ")|join("\n                - ")|replace("=", ": ") }}

        Exec call from the CLI:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}
    '''
"""


DELETE = """
async def {{function.name}}(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              {{ function.ref }}.absent:
                - {{ function.required_call_params.split(", ")|join("\n                - ")|replace("=", ": ") }}

        Exec call from the CLI:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}
    '''
"""

GET = """
async def {{function.name}}(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: {{ function.ref }}.{{ function.name }}
                - kwargs:
                  {{ function.required_call_params.split(", ")|join("\n" + " " * 18)|replace("=", ": ") }}

        Exec call from the CLI:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}
    '''
"""

LIST = """
async def list_(hub, ctx{{function.header_params}}) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: {{ function.ref }}.{{ function.name }}
                - kwargs:
                  {{ function.required_call_params.split(", ")|join("\n" + " " * 18)|replace("=", ": ") }}

        Exec call from the CLI:

        .. code-block:: bash

            idem exec {{ function.ref }}.{{ function.name }} {{ function.required_call_params }}

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe {{ function.ref }}

    '''
"""
