from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from apps.core.base_model import Base


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