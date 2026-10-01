from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["Низкий", "Средний", "Высокий"]


class PartyDataSchema(BaseModel):
    name: str
    inn: str
    ogrn: str | None = None
    kpp: str | None = None
    legal_form: str | None = None
    okved: str | None = None
    manager_position: str | None = None
    director: str | None = None
    address: str | None = None
    city: str | None = None
    registration_date: date | None = None
    authorized_capital: Decimal | None = None
    status: str | None = None
    risk_level: RiskLevel | None = None
    risk_factors: list[str] = Field(default_factory=list)


class PartyCheckRequest(BaseModel):
    inn: str = Field(pattern=r"^\d{10}(\d{2})?$")


class PartySearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=300)
    count: int = Field(default=10, ge=1, le=20)


class PartySearchResult(BaseModel):
    name: str
    inn: str | None = None
    ogrn: str | None = None
    director: str | None = None
    city: str | None = None
    address: str | None = None
    status: str | None = None


class EscrowCreateRequest(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str = Field(min_length=2, max_length=1000)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    buyer_inn: str = Field(pattern=r"^\d{10}(\d{2})?$")
    seller_inn: str = Field(pattern=r"^\d{10}(\d{2})?$")


class EscrowResponse(BaseModel):
    hold_id: str
    status: str
    amount: Decimal
    message: str


class EscrowReleaseRequest(BaseModel):
    hold_id: str
