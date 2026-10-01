from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_party_provider, get_payment_provider, get_settings
from backend.providers.base import BasePartyProvider, BasePaymentProvider
from backend.schemas import EscrowCreateRequest, EscrowReleaseRequest, EscrowResponse, PartyCheckRequest, PartyDataSchema, PartySearchRequest, PartySearchResult
from backend.services.risk_analyzer import RiskAnalyzer

settings = get_settings()
app = FastAPI(title="Smart Retail API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/party/check", response_model=PartyDataSchema)
async def check_party(payload: PartyCheckRequest, provider: BasePartyProvider = Depends(get_party_provider)):
    return RiskAnalyzer().analyze(await provider.get_party_info(payload.inn))


@app.post("/api/v1/party/search", response_model=list[PartySearchResult])
async def search_parties(payload: PartySearchRequest, provider: BasePartyProvider = Depends(get_party_provider)):
    return await provider.search_parties(payload.query, payload.count)


@app.post("/api/v1/deals/create-escrow", response_model=EscrowResponse)
async def create_escrow(payload: EscrowCreateRequest, provider: BasePaymentProvider = Depends(get_payment_provider)):
    return await provider.create_hold(**payload.model_dump())


@app.post("/api/v1/deals/release-escrow", response_model=EscrowResponse)
async def release_escrow(payload: EscrowReleaseRequest, provider: BasePaymentProvider = Depends(get_payment_provider)):
    return await provider.release_hold(payload.hold_id)
