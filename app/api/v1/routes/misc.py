from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.core.config.settings import settings

router = APIRouter()


@router.get("/health")
async def health() -> bool:
    return True


@router.get("/", response_class=PlainTextResponse)
async def index() -> str:
    base = settings.API_V1_STR
    return (
        "softForMarket — GGSEL & Digiseller → Telegram + TeaTeaGram\n"
        f"{base}/status?code={{uuid}}              — статус заказа\n"
        f"{base}/ggsel?uniquecode={{uuid}}         — GGSEL callback\n"
        f"{base}/digiseller-callback?uniquecode={{uuid}} — PLATI callback\n"
    )
