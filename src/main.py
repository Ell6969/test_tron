import asyncio

from fastapi import FastAPI, Request

from src.dependencies import PaginationDep, TronAccountInfoDep
from src.schemas import SHystoryRequestAll, SInfoTronResult, SLogsResult
from src.service import HistoryWalletRequestService

app = FastAPI()


@app.get("/logs")
async def get_logs(
    pagination: PaginationDep,
) -> SLogsResult:
    """
    Получить логи запросов
    """
    res = await HistoryWalletRequestService.get_last_records(pagination)
    return SLogsResult(logs=res)


TEST_ADRES = "TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf"


@app.post("/main")
async def get_info_tron(
    client_info: TronAccountInfoDep,
    request: Request,
) -> SInfoTronResult:
    """
    Запросить данные трон по адресу
    """
    from src.tasks import run_add_history

    ip = request.headers.get("x-forwarded-for") or request.client.host
    data = SHystoryRequestAll(ip=ip, **client_info.model_dump(exclude_none=True))
    asyncio.create_task(run_add_history(data))
    return SInfoTronResult(result=client_info)
