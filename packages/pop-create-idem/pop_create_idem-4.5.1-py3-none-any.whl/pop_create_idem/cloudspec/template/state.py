"""
Templates for state modules
"""

PRESENT_FUNCTION = """
async def {{function.name}}(
    hub,
    ctx
    {% if function.header_params %}
        {{function.header_params}}
    {% endif -%},
) -> Dict[str, Any]:
    '''{{function.doc|replace("'" * 3, '"' * 3)}}
    Example:
        .. code-block:: sls

          {% if function.example_request_syntax %}
          {{ function.example_request_syntax|indent(12) }}
          {% else %}
              resource_is_{{function.name}}:
                {{ function.ref }}.{{ function.name }}:
                  - {{ function.required_call_params.split(", ")|join("\n                  - ")|replace("=", ": ") }}
          {% endif %}
    '''
"""

ABSENT_FUNCTION = """
async def {{function.name}}(
    hub,
    ctx
    {% if function.header_params %}
        {{function.header_params}}
    {% endif -%},
)  -> Dict[str, Any]:
    '''
    {{function.doc|replace("'" * 3, '"' * 3)}}
    Example:
        .. code-block:: sls

            {% if function.example_request_syntax %}
            {{ function.example_request_syntax|indent(12) }}
            {% else %}
                resource_is_{{function.name}}:
                  {{ function.ref }}.{{ function.name }}:
                    - name: value
                    - resource_id: value
            {% endif %}
    '''
"""

DESCRIBE_FUNCTION = """
async def {{function.name}}(hub, ctx) -> Dict[str, Dict[str, Any]]:
    '''
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    {{function.doc|replace("'" * 3, '"' * 3)}}
    Example:

        .. code-block:: bash

            $ idem describe {{ function.ref }}
    '''
"""
