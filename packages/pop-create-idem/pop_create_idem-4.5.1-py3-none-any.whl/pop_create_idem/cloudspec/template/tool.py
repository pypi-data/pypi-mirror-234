FUNCTION = """
async def {{function.name}}(
    hub,
    ctx{{function.header_params}}
) -> Dict[str, Any]:
    r\"""
    {{function.doc|replace("'" * 3, '"' * 3)}}
    \"""
"""
