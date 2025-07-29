from src.schemas import SHystoryRequestAll
from src.service import HistoryWalletRequestService


async def run_add_history(data: SHystoryRequestAll):
    await HistoryWalletRequestService.add_history(data)
