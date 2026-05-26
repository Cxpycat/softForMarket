from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from loguru import logger

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        logger.warning("Попытка доступа к API без ключа")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API ключ не предоставлен")

    return api_key
