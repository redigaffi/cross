import pytest
import respx
from cashews import cache

from cross.client import CrossmintClient
from cross.config import Config


@pytest.fixture(autouse=True)
async def invalidate_cache():
    await cache.delete_match("*")


@pytest.fixture(autouse=True)
def mock_respx():
    respx.mock.clear()
    respx.clear()
    respx.delete("*")


@pytest.fixture
def client():
    client = CrossmintClient(Config().BASE_URL)
    yield client
    del client
