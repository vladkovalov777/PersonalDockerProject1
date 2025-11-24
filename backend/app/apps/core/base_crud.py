from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from apps.core.base_model import Base
from sqlalchemy import select


class BaseCRUDManager(ABC):
    model: type[Base] = None

    @abstractmethod
    def __init__(self):
        # set model
        pass

    async def create(self, *, session: AsyncSession, **kwargs) -> Base:
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    async def get(self, *,  session: AsyncSession, model_field, value) -> Optional[Base]:
        query = select(self.model).filter(model_field == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()