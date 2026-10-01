import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from backend.schemas import PartyDataSchema, RecentPartySchema


class SearchHistory:
    def __init__(self) -> None:
        self.path = Path(__file__).resolve().parent.parent / "smart_retail_history.db"
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS party_history (
                inn TEXT PRIMARY KEY, name TEXT NOT NULL, ogrn TEXT, director TEXT,
                city TEXT, address TEXT, status TEXT, checked_at TEXT NOT NULL)"""
            )

    def _connect(self):
        return sqlite3.connect(self.path)

    def add(self, party: PartyDataSchema) -> None:
        checked_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO party_history (inn,name,ogrn,director,city,address,status,checked_at)
                VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(inn) DO UPDATE SET
                name=excluded.name, ogrn=excluded.ogrn, director=excluded.director,
                city=excluded.city, address=excluded.address, status=excluded.status,
                checked_at=excluded.checked_at""",
                (party.inn, party.name, party.ogrn, party.director, party.city, party.address, party.status, checked_at),
            )

    def recent(self, limit: int = 8) -> list[RecentPartySchema]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT name,inn,ogrn,director,city,address,status,checked_at FROM party_history "
                "ORDER BY checked_at DESC LIMIT ?", (limit,)
            ).fetchall()
        fields = ("name", "inn", "ogrn", "director", "city", "address", "status", "checked_at")
        return [RecentPartySchema(**dict(zip(fields, row))) for row in rows]
