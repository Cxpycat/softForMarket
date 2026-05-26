from typing import Any, Literal

import httpx
from loguru import logger

DEFAULT_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)


class BaseApi:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url or "",
            timeout=timeout,
            headers=headers or {},
            limits=DEFAULT_LIMITS,
            transport=httpx.AsyncHTTPTransport(retries=3),
            proxy=proxy,
            follow_redirects=True,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: Any | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        response_type: Literal["json", "text", "response"] = "json",
    ) -> Any:
        r = await self._perform(method, url, params=params, json_data=json_data, data=data, headers=headers)
        if response_type == "response":
            return r
        if response_type == "text":
            return r.text
        return r.json()

    async def _perform(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: Any | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        try:
            r = await self._client.request(method, url, params=params, json=json_data, data=data, headers=headers)
            r.raise_for_status()
            return r
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Сервис вернул ошибку: {method} {exc.request.url} -> {exc.response.status_code} {exc.response.text[:200]}"
            )
            raise
        except httpx.RequestError as exc:
            logger.error(f"Ошибка сетевого запроса: {method} {url} -> {exc}")
            raise
