from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.core.config.settings import settings


class Base(DeclarativeBase):
    metadata = MetaData(schema=settings.POSTGRES_SCHEMA)
