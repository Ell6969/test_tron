import pytest

from src.base_dao import HistoryWalletRequestDAO, SHystoryRequestAll


@pytest.mark.parametrize(
    "energy,trx,address_wallet,ip,created_at",
    [
        (
            11111111,
            "313471.3022520000",
            "TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
            "127.0.0.1",
            "2025-07-29T17:10:08.020250",
        ),
    ],
)
async def test_add_history(energy, trx, address_wallet, ip, created_at):
    data = SHystoryRequestAll(energy=energy, trx=trx, address_wallet=address_wallet, ip=ip, created_at=created_at)
    log = await HistoryWalletRequestDAO.add(**data.model_dump(exclude_none=True))

    assert log
    assert log.energy == 11111111
