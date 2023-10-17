TEST_FUNCTION = """
@pytest.mark.asyncio
{% if function.hardcoded.parametrize %}@pytest.mark.parametrize(**PARAMETRIZE){% endif %}
async def {{function.name}}(hub, ctx{% if function.hardcoded.parametrize %}, __test{% endif %}):
    r'''
    **Test function**
    '''
"""
