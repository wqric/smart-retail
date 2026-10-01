from abc import ABC, abstractmethod

from backend.schemas import EscrowResponse, PartyDataSchema, PartySearchResult


class BasePartyProvider(ABC):
    @abstractmethod
    async def get_party_info(self, inn: str) -> PartyDataSchema:
        """Return verified counterparty data for an INN."""

    @abstractmethod
    async def search_parties(self, query: str, count: int = 10) -> list[PartySearchResult]:
        """Search counterparties by a free-form query."""


class BasePaymentProvider(ABC):
    @abstractmethod
    async def create_hold(self, *, title: str, description: str, amount, buyer_inn: str, seller_inn: str) -> EscrowResponse:
        """Create an escrow hold."""

    @abstractmethod
    async def release_hold(self, hold_id: str) -> EscrowResponse:
        """Release an existing escrow hold."""
