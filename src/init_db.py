import asyncio

from src.databases import Base, engine
from src.models import HistoryWalletRequest


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы.")


if __name__ == "__main__":
    asyncio.run(init_models())
