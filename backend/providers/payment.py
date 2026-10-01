from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException

from backend.providers.base import BasePaymentProvider
from backend.schemas import EscrowResponse


class MockPaymentProvider(BasePaymentProvider):
    async def create_hold(self, *, title: str, description: str, amount: Decimal, buyer_inn: str, seller_inn: str) -> EscrowResponse:
        return EscrowResponse(hold_id=f"mock_hold_{uuid4().hex[:12]}", status="held", amount=amount, message="Средства успешно заморожены на эскроу-счёте")

    async def release_hold(self, hold_id: str) -> EscrowResponse:
        return EscrowResponse(hold_id=hold_id, status="released", amount=Decimal("0"), message="Средства перечислены получателю")


class YookassaEscrowProvider(BasePaymentProvider):
    async def create_hold(self, **kwargs) -> EscrowResponse:
        # TODO: create YooKassa payment with capture=False and persist provider payment ID.
        raise HTTPException(status_code=501, detail="Интеграция ЮKassa пока не подключена")

    async def release_hold(self, hold_id: str) -> EscrowResponse:
        # TODO: capture the YooKassa payment tied to hold_id after deal confirmation.
        raise HTTPException(status_code=501, detail="Интеграция ЮKassa пока не подключена")
