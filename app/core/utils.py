from collections.abc import Sequence
from typing import Any, Literal, TypeVar

from fastapi import HTTPException, status
import httpx
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

Schema = TypeVar("Schema", bound=BaseModel)


def to_schema(
    model: DeclarativeBase,
    schema_cls: type[Schema],
) -> Schema:
    return schema_cls.model_validate(model)


def to_schema_list(
    models: Sequence[DeclarativeBase],
    schema_cls: type[Schema],
) -> list[Schema]:
    return [to_schema(m, schema_cls) for m in models]


async def make_request(
    method: Literal["GET", "POST", "PUT", "DELETE"],
    url: str,
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
                timeout=60.0,
            )
        except httpx.HTTPError as e:
            logger.error(f"Ошибка при взаимодействии с сервером: {e.__class__.__name__} {e!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при взаимодействии с сервером: {e!s}",
            )
        try:
            response.raise_for_status()
            return response.json()  # type: ignore
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP-ошибка для {e.request.url}: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Ошибка запроса для {e.request.url}: {e}")
            raise
