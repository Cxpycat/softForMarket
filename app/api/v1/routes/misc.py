from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/health")
async def health() -> bool:
    return True


@router.get("/", response_class=PlainTextResponse)
async def index() -> str:
    return (
        "softForMarket — GGSEL & Digiseller → Telegram + TeaTeaGram\n"
        "/status?code={uuid}              — статус заказа\n"
        "/ggsel?uniquecode={uuid}         — GGSEL callback\n"
        "/digiseller-callback?uniquecode={uuid} — PLATI callback\n"
    )
