import pytest
from httpx import AsyncClient
from respx import MockRouter
from src.tarotai.ai.clients.providers.deepseek_v3 import DeepSeekClient
from src.tarotai.ai.clients.providers.voyage import VoyageClient

@pytest.fixture
async def mock_deepseek():
    async with AsyncClient(base_url="http://test") as client:
        yield DeepSeekClient(api_key="test", client=client)

@pytest.fixture
async def mock_voyage():
    async with AsyncClient(base_url="http://test") as client:
        yield VoyageClient(api_key="test", client=client)

@pytest.fixture
async def mock_server():
    async with MockRouter() as respx_mock:
        yield respx_mock
