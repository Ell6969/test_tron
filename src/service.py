from src.base_dao import HistoryWalletRequestDAO
from src.dependencies import SFilterPagination
from src.schemas import SHystoryRequestAll


class HistoryWalletRequestService:

    @classmethod
    async def get_last_records(
        cls,
        pagination: SFilterPagination,
    ):
        res = await HistoryWalletRequestDAO.find_all(pagination)
        return res

    @classmethod
    async def add_history(
        cls,
        data: SHystoryRequestAll,
    ):
        res = await HistoryWalletRequestDAO.add(**data.model_dump(exclude_none=True))
        return res
