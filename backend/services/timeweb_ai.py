import json
import logging
import re

import httpx
from fastapi import HTTPException

from backend.config import Settings
from backend.schemas import AiAnalysisResponse, PartyDataSchema

logger = logging.getLogger(__name__)


class TimewebAiService:
    """Creates a concise business brief from the verified DaData card."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def analyze(self, party: PartyDataSchema) -> AiAnalysisResponse:
        if not self.settings.timeweb_ai_token or not self.settings.timeweb_agent_access_id:
            raise HTTPException(
                status_code=503,
                detail="ИИ-анализ не настроен: добавьте TIMEWEB_AI_TOKEN и TIMEWEB_AGENT_ACCESS_ID в backend/.env.",
            )

        context = json.dumps(party.model_dump(mode="json"), ensure_ascii=False)
        prompt = (
            "Проанализируй карточку российского контрагента. Используй только переданные данные, "
            "не выдумывай сведения о судах, финансах, санкциях и долгах. Верни ТОЛЬКО валидный JSON "
            "без Markdown по схеме: {\"summary\": string, \"risk_focus\": [string], "
            "\"recommendations\": [string]}. Summary — 2–4 нейтральных предложения; "
            "в каждом массиве максимум 4 коротких пункта. Данные: " + context
        )
        url = (
            "https://agent.timeweb.cloud/api/v1/cloud-ai/agents/"
            f"{self.settings.timeweb_agent_access_id}/v1/chat/completions"
        )
        payload = {
            "model": self.settings.timeweb_ai_model,
            "messages": [
                {"role": "system", "content": "Ты риск-аналитик B2B. Отвечай строго в указанном JSON-формате."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0, trust_env=True) as client:
                response = await client.post(
                    url,
                    headers={"Authorization": f"Bearer {self.settings.timeweb_ai_token}"},
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.warning("Timeweb AI returned %s", exc.response.status_code)
            raise HTTPException(status_code=502, detail="Сервис ИИ-анализа временно отклонил запрос.") from exc
        except httpx.RequestError as exc:
            logger.exception("Timeweb AI network error: %s", exc)
            raise HTTPException(status_code=502, detail="Не удалось связаться с сервисом ИИ-анализа.") from exc

        try:
            content = response.json()["choices"][0]["message"]["content"].strip()
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.IGNORECASE)
            return AiAnalysisResponse.model_validate_json(content)
        except (KeyError, IndexError, json.JSONDecodeError, ValueError) as exc:
            logger.warning("Timeweb AI returned an unexpected answer format")
            raise HTTPException(status_code=502, detail="ИИ вернул ответ в неподдерживаемом формате. Повторите попытку.") from exc
