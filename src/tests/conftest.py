import asyncio
import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from src.databases import Base, async_session_maker, engine
from src.main import app as fastapi_app
from src.models import HistoryWalletRequest


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    logs = open_mock_json("history_wallet_request")
    for log in logs:
        log["created_at"] = datetime.fromisoformat(log["created_at"])

    async with async_session_maker() as session:
        for Model, values in [
            (HistoryWalletRequest, logs),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
