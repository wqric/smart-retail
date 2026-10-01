from datetime import date

from backend.schemas import PartyDataSchema


class RiskAnalyzer:
    def analyze(self, party: PartyDataSchema) -> PartyDataSchema:
        factors: list[str] = []
        score = 0
        if party.status and party.status.upper() not in {"ACTIVE", "ДЕЙСТВУЮЩЕЕ"}:
            factors.append("Статус организации требует дополнительной проверки")
            score += 3
        if not party.director:
            factors.append("Не найдены сведения о руководителе")
            score += 1
        if party.registration_date and (date.today() - party.registration_date).days < 180:
            factors.append("Компания зарегистрирована менее шести месяцев назад")
            score += 1
        if not party.authorized_capital or party.authorized_capital < 10000:
            factors.append("Низкий или отсутствующий уставный капитал")
            score += 1
        party.risk_level = "Высокий" if score >= 3 else "Средний" if score else "Низкий"
        party.risk_factors = factors or ["Критичных факторов риска не обнаружено"]
        return party
