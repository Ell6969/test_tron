from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
from tronpy import Tron

from src.schemas import SAddressHystoryRequest, SAddressInfo


class SFilterPagination(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы для пагинации")
    page_size: int = Field(5, ge=1, le=100, description="Количество элементов на странице, максимум 100")


async def get_tron_address_info(address: SAddressHystoryRequest) -> SAddressInfo:
    try:
        client = Tron(network="nile", conf={"timeout": 20.0})
        resources = client.get_account_resource(address.address_wallet)

        balance_trx = client.get_account_balance(address.address_wallet)
        bandwidth = client.get_bandwidth(address.address_wallet)
        energy = resources.get("TotalEnergyLimit", 0)

        return SAddressInfo(
            address_wallet=address.address_wallet,
            trx=balance_trx,
            bandwidth=bandwidth,
            energy=energy,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения данных из Tron: {str(e)}")


TronAccountInfoDep = Annotated[SAddressInfo, Depends(get_tron_address_info)]
PaginationDep = Annotated[SFilterPagination, Depends(SFilterPagination)]
