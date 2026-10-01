import subprocess

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from backend.config import get_party_provider, get_payment_provider, get_settings
from backend.providers.base import BasePartyProvider, BasePaymentProvider
from backend.schemas import AiAnalysisRequest, AiAnalysisResponse, EscrowCreateRequest, EscrowReleaseRequest, EscrowResponse, PartyCheckRequest, PartyDataSchema, PartySearchRequest, PartySearchResult
from backend.services.risk_analyzer import RiskAnalyzer
from backend.services.timeweb_ai import TimewebAiService
from backend.services.history import SearchHistory
from backend.services.pdf_extract import create_extract_pdf

settings = get_settings()
app = FastAPI(title="Smart Retail API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
history = SearchHistory()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/party/check", response_model=PartyDataSchema)
async def check_party(payload: PartyCheckRequest, provider: BasePartyProvider = Depends(get_party_provider)):
    party = RiskAnalyzer().analyze(await provider.get_party_info(payload.inn))
    history.add(party)
    return party


@app.get("/api/v1/party/history")
async def get_party_history():
    return history.recent()


@app.post("/api/v1/party/extract-pdf")
async def download_party_extract(payload: PartyDataSchema):
    try:
        document = create_extract_pdf(payload)
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        raise HTTPException(status_code=500, detail="Не удалось сформировать PDF-выписку.") from exc
    return Response(
        content=document,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="extract-{payload.inn}.pdf"'},
    )


@app.post("/api/v1/party/search", response_model=list[PartySearchResult])
async def search_parties(payload: PartySearchRequest, provider: BasePartyProvider = Depends(get_party_provider)):
    return await provider.search_parties(payload.query, payload.count)


@app.post("/api/v1/party/ai-analysis", response_model=AiAnalysisResponse)
async def get_ai_analysis(payload: AiAnalysisRequest):
    return await TimewebAiService(get_settings()).analyze(payload.party)


@app.post("/api/v1/deals/create-escrow", response_model=EscrowResponse)
async def create_escrow(payload: EscrowCreateRequest, provider: BasePaymentProvider = Depends(get_payment_provider)):
    return await provider.create_hold(**payload.model_dump())


@app.post("/api/v1/deals/release-escrow", response_model=EscrowResponse)
async def release_escrow(payload: EscrowReleaseRequest, provider: BasePaymentProvider = Depends(get_payment_provider)):
    return await provider.release_hold(payload.hold_id)
