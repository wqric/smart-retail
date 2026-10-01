from datetime import date
import logging

import httpx
from fastapi import HTTPException

from backend.providers.base import BasePartyProvider
from backend.schemas import PartyDataSchema, PartySearchResult

logger = logging.getLogger(__name__)


class DaDataPartyProvider(BasePartyProvider):
    endpoint = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
    suggest_endpoint = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"

    def __init__(self, api_key: str, secret_key: str | None = None) -> None:
        self.api_key = api_key
        self.secret_key = secret_key

    async def get_party_info(self, inn: str) -> PartyDataSchema:
        headers = {"Authorization": f"Token {self.api_key}"}
        if self.secret_key:
            headers["X-Secret"] = self.secret_key
        try:
            async with httpx.AsyncClient(verify=False, trust_env=True, timeout=10.0) as client:
                response = await client.post(self.endpoint, headers=headers, json={"query": inn})
        except httpx.RequestError as exc:
            logger.exception("DaData request failed for INN %s: %s", inn, exc)
            raise HTTPException(status_code=502, detail="Сервис DaData временно недоступен") from exc
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="Не удалось получить данные DaData")
        suggestions = response.json().get("suggestions", [])
        if not suggestions:
            raise HTTPException(status_code=404, detail="Контрагент с таким ИНН не найден")
        data = suggestions[0]["data"]
        reg = data.get("state", {}).get("registration_date")
        return PartyDataSchema(
            name=data.get("name", {}).get("full_with_opf") or suggestions[0].get("value", inn),
            inn=data.get("inn", inn), ogrn=data.get("ogrn"), kpp=data.get("kpp"),
            legal_form=(data.get("opf") or {}).get("full"), okved=data.get("okved"),
            manager_position=(data.get("management") or {}).get("post"),
            director=(data.get("management") or {}).get("name"),
            address=(data.get("address") or {}).get("unrestricted_value"),
            city=(data.get("address") or {}).get("data", {}).get("city"),
            registration_date=date.fromtimestamp(reg / 1000) if reg else None,
            authorized_capital=(data.get("capital") or {}).get("value"),
            status=(data.get("state") or {}).get("status"),
        )

    async def search_parties(self, query: str, count: int = 10) -> list[PartySearchResult]:
        headers = {"Authorization": f"Token {self.api_key}"}
        if self.secret_key:
            headers["X-Secret"] = self.secret_key
        try:
            async with httpx.AsyncClient(verify=False, trust_env=True, timeout=10.0) as client:
                response = await client.post(self.suggest_endpoint, headers=headers, json={"query": query, "count": count})
        except httpx.RequestError as exc:
            logger.exception("DaData search failed for query %r: %s", query, exc)
            raise HTTPException(status_code=502, detail="Сервис DaData временно недоступен") from exc
        if response.status_code >= 400:
            logger.warning("DaData search returned %s: %s", response.status_code, response.text)
            raise HTTPException(status_code=502, detail="DaData отклонил поисковый запрос")
        results: list[PartySearchResult] = []
        for item in response.json().get("suggestions", []):
            data = item.get("data") or {}
            address = (data.get("address") or {}).get("unrestricted_value")
            city = (data.get("address") or {}).get("data", {}).get("city")
            results.append(PartySearchResult(
                name=data.get("name", {}).get("full_with_opf") or item.get("value", "Без названия"),
                inn=data.get("inn"), ogrn=data.get("ogrn"),
                director=(data.get("management") or {}).get("name"),
                city=city, address=address, status=(data.get("state") or {}).get("status"),
            ))
        return results


class FnsPartyProvider(BasePartyProvider):
    async def get_party_info(self, inn: str) -> PartyDataSchema:
        # TODO: integrate the official FNS service when stable API credentials are available.
        raise HTTPException(status_code=501, detail="Провайдер ФНС пока не подключён")

    async def search_parties(self, query: str, count: int = 10) -> list[PartySearchResult]:
        raise HTTPException(status_code=501, detail="Поиск через ФНС пока не подключён")
