"""Add test related fixtures here e.g. a fixture that will pre-create a resource needed for the tests."""


import asyncio
import pathlib
from typing import Dict, Any, List

import dict_tools
import pytest_asyncio

import pop

import pytest


@pytest.fixture(scope="session")
def code_dir() -> pathlib.Path:
    print(f"code_dir:{pathlib.Path(__file__).parent.parent.absolute()}")
    return pathlib.Path(__file__).parent.parent.absolute()


@pytest.fixture(scope="module")
def acct_data(ctx):
    """
    acct_data that can be used in running simple yaml blocks
    """
    yield {"profiles": {"{{cookiecutter.service_name}}": {"default": ctx.acct}}}


@pytest.fixture(scope="module", autouse=True)
def acct_profile() -> str:
    return "TODO: Add profile name to use for test"


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def acct_subs():
    return ["{{cookiecutter.service_name}}"]


@pytest.fixture(scope="module", name="hub")
def integration_hub(code_dir, event_loop):
    hub = pop.hub.Hub()
    hub.pop.loop.CURRENT_LOOP = event_loop
    hub.pop.sub.add(dyne_name="idem")
    hub.pop.config.load(hub.idem.CONFIG_LOAD, "idem", parse_cli=False)
    hub.idem.RUNS = {"test": {}}

    yield hub


@pytest_asyncio.fixture(scope="module", name="ctx")
async def integration_ctx(
    hub, acct_subs: List[str], acct_profile: str
) -> Dict[str, Any]:
    ctx = dict_tools.data.NamespaceDict(
        run_name="test",
        test=False,
        tag="fake_|-test_|-tag",
        old_state={},
    )

    if not hub.OPT.acct.acct_file:
        raise ConnectionError("No ACCT_FILE in the environment")
    if not hub.OPT.acct.acct_key:
        raise ConnectionError("No ACCT_KEY in the environment")

    await hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
    ctx.acct = await hub.acct.init.gather(acct_subs, acct_profile)
    if not ctx.acct:
        raise Exception(
            f'Unable to load acct "{acct_profile}" from "{hub.OPT.acct.acct_file}"'
        )

    yield ctx


@pytest.fixture(
    scope="function",
    name="__test",
    params=[0, 1, 2, 3],
    ids=["--test", "run", "no change --test", "no change"],
)
def test_flag(ctx, request):
    """
    Functions that use the __test fixture will be run four times
    0. With the --test flag set, to test what happens before creating a resource
    1. Without the --test flag set, to create a resource
    2. With the --test flag set, to verify that no changes would be made
    3. Without the --test flag set, to verify that no changes are made
    """
    ctx.test = bool((request.param + 1) % 2)
    yield request.param
