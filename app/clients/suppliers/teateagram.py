from typing import Any

from loguru import logger

from app.clients.base import BaseApi
from app.core.config.settings import settings

TEA_API_BASE = "https://teateagram.com/api/v2"


class TeaTeaGramApi(BaseApi):
    async def create_supplier_order(self, service_id: int, link: str, quantity: int) -> dict[str, Any]:
        payload = {
            "key": settings.TEA_API_KEY.get_secret_value(),
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity,
        }
        logger.info(f"[SUPPLIER] add service={service_id} link={link} qty={quantity}")
        data: dict[str, Any] = await self.request("POST", TEA_API_BASE, data=payload)
        if "order" not in data:
            raise RuntimeError(f"Поставщик не принял заказ: {data}")
        return data

    async def get_supplier_status(self, order_id: str) -> dict[str, Any]:
        payload = {"key": settings.TEA_API_KEY.get_secret_value(), "action": "status", "order": order_id}
        result: dict[str, Any] = await self.request("POST", TEA_API_BASE, data=payload)
        return result


teateagram = TeaTeaGramApi()
