from unittest import mock

import pytest


@pytest.fixture(scope="session", name="hub")
def unit_hub(hub):
    hub.pop.sub.add(dyne_name="idem")
    yield hub


async def _setup_hub(hub):
    # Set up the hub before each function here
    ...


async def _teardown_hub(hub):
    # Clean up the hub after each function here
    ...


@pytest.fixture(scope="function", autouse=True)
async def function_hub_wrapper(hub):
    await _setup_hub(hub)
    yield
    await _teardown_hub(hub)


@pytest.fixture(scope="function")
def mock_hub(hub):
    m_hub = hub.pop.testing.mock_hub()
    m_hub.OPT = mock.MagicMock()
    yield m_hub
