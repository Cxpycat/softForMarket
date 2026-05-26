import asyncio
from datetime import datetime
import hashlib
import time
from typing import Any

import httpx
from loguru import logger

from app.clients.base import BaseApi
from app.core.config.settings import settings

DIGI_LOGIN_URL = "https://api.digiseller.com/api/apilogin"
DIGI_UNIQUE_URL = "https://api.digiseller.com/api/purchases/unique-code/{code}?token={token}"
DIGI_UNIQUE_URL_RESERVE = "https://oplata.info/api/purchases/unique-code/{code}?token={token}"


def _parse_valid_thru(value: str) -> float | None:
    if not value:
        return None
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    if "." in s:
        head, tail = s.split(".", 1)
        if "+" in tail or "-" in tail:
            sign = "+" if "+" in tail else "-"
            frac, tz = tail.split(sign, 1)
            frac = (frac + "000000")[:6]
            s = f"{head}.{frac}{sign}{tz}"
        else:
            frac = (tail + "000000")[:6]
            s = f"{head}.{frac}"
    try:
        return datetime.fromisoformat(s).timestamp()
    except ValueError:
        return None


class DigisellerApi(BaseApi):
    def __init__(self, timeout: float = 25.0) -> None:
        super().__init__(timeout=timeout)
        self._token: str | None = None
        self._expiry: float = 0.0
        self._lock = asyncio.Lock()

    async def _get_token(self) -> str:
        now = time.time()
        async with self._lock:
            if self._token and now < self._expiry - 30:
                return self._token
            ts = int(now)
            sign = hashlib.sha256((settings.DIGI_API_KEY.get_secret_value() + str(ts)).encode()).hexdigest()
            payload = {"seller_id": int(settings.DIGI_SELLER_ID), "timestamp": ts, "sign": sign}
            data = await self.request("POST", DIGI_LOGIN_URL, json_data=payload)
            if int(data.get("retval", -999)) != 0:
                raise RuntimeError(f"Ошибка логина Digiseller: {data}")
            self._token = data.get("token") or ""
            self._expiry = _parse_valid_thru(data.get("valid_thru", "")) or (now + 110 * 60)
            return self._token

    async def _get_purchase_raw(self, url_tpl: str, code: str, token: str) -> httpx.Response:
        # без raise_for_status — статусы разбираем вручную (401, фолбэк на резерв)
        return await self._client.get(url_tpl.format(code=code, token=token))

    async def get_purchase(self, unique_code: str) -> dict[str, Any]:
        token = await self._get_token()
        resp = await self._get_purchase_raw(DIGI_UNIQUE_URL, unique_code, token)
        if resp.status_code == 401:
            async with self._lock:
                self._token, self._expiry = None, 0.0
            token = await self._get_token()
            resp = await self._get_purchase_raw(DIGI_UNIQUE_URL, unique_code, token)

        if resp.status_code != 200:
            resp_reserve = await self._get_purchase_raw(DIGI_UNIQUE_URL_RESERVE, unique_code, token)
            if resp_reserve.status_code != 200:
                raise RuntimeError(
                    f"unique-code HTTP {resp.status_code}/{resp_reserve.status_code}: {resp.text} // {resp_reserve.text}"
                )
            logger.info(f"[DIGI] заказ {unique_code} через резерв")
            data: dict[str, Any] = resp_reserve.json()
            return data

        logger.info(f"[DIGI] заказ {unique_code} получен")
        result: dict[str, Any] = resp.json()
        return result


digiseller = DigisellerApi(timeout=25.0)
