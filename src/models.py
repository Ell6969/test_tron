from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, text
from sqlalchemy.orm import Mapped, mapped_column

from src.databases import Base


class HistoryWalletRequest(Base):
    __tablename__ = "history_wallet_request"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(default="")
    address_wallet: Mapped[str] = mapped_column(default="", comment="Адрес кошелька")
    bandwidth: Mapped[int] = mapped_column(default=0)
    energy: Mapped[int] = mapped_column(default=0)
    trx: Mapped[Decimal] = mapped_column(
        Numeric,
        default=Decimal("0.0"),
        server_default=text("0.0"),
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, comment="Дата создания")

    def __str__(self):
        return f"id: {self.id} | adress: {self.address_wallet}"
