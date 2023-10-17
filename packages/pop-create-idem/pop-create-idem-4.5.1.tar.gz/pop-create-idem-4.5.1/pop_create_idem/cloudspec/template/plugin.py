"""
Templates for plugins
"""

HEADER = '''
"""{{ resource_header }} {{ plugin.doc }}"""

{% if plugin.imports -%}
{{ plugin.imports|join('\n') }}
{%- endif %}

{% if plugin.virtual_imports -%}
try:
    {{ plugin.virtual_imports|join('\n') }}
    HAS_LIBS = True,
except ImportError as e:
    HAS_LIBS = False, str(e)
{%- endif %}

{%- if plugin.contracts -%}
__contracts__ = {{plugin.contracts}}
{%- endif %}

{%- if plugin.virtual_imports -%}
def __virtual__(hub):
    return HAS_LIBS
{%- endif %}

{%- if plugin.virtualname -%}
__virtualname__ = "{{plugin.virtualname}}"
{%- endif %}

{%- if plugin.sub_alias -%}
__sub_alias__ = {{plugin.sub_alias}}
{%- endif %}

{% if plugin.func_alias -%}
__func_alias__ = {{plugin.func_alias}}
{% endif %}

{% if plugin.file_vars %}
{% for var, val in plugin.file_vars.items() %}
{{ var }} = {{ val }}
{% endfor %}
{% endif %}
'''
