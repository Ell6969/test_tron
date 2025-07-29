from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class SAddressHystoryRequest(BaseModel):
    address_wallet: str = Field(default="", description="Адрес кошелька")

    model_config = {"from_attributes": True}


class SAddressInfo(SAddressHystoryRequest):
    bandwidth: int = Field(default=0)
    energy: int = Field(default=0)
    trx: Decimal = Field(default=Decimal("0.0"), ge=0)

    model_config = {"from_attributes": True}


class SHystoryRequestAll(SAddressInfo):
    id: int | None = None
    ip: str = ""
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class SLogsResult(BaseModel):
    logs: List[SHystoryRequestAll]

    model_config = {"from_attributes": True}


class SInfoTronResult(BaseModel):
    result: SAddressInfo

    model_config = {"from_attributes": True}
