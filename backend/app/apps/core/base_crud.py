from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from apps.core.base_model import Base
from sqlalchemy import select, and_, or_


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

    async def get_items(self, *, session: AsyncSession, q: str = '', search_fields: list = None):
        query = select(self.model)
        if q and search_fields:
            words = [word for word in q.replace(',', ' ').split() if len(word) > 1]
            search_fields_condition = or_(
                and_(*(search_field.icontains(word) for word in words))
                for search_field in search_fields
            )
            query = query.filter(search_fields_condition)

        result = await session.execute(query)
        return result.scalars()