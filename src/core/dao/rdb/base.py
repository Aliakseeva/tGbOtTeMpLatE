from dataclasses import dataclass
from contextlib import suppress
from typing import Any, TypeVar, Generic, Type, Sequence

from sqlalchemy.exc import IntegrityError

from sqlalchemy import select, ScalarResult, Result, delete, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.core.db.models import Base

Model = TypeVar("Model", bound=Base, covariant=True, contravariant=False)


@dataclass
class BaseDAO(Generic[Model]):
    model: Type[Model]
    session: AsyncSession

    async def _get_one_by_id(self, id_: int) -> Model:
        one = await self.session.execute(
            select(self.model).where(self.model.id_ == id_)
        )
        return one.scalar()

    async def _get_list(self) -> Sequence[Model]:
        list_: Result[Model] = await self.session.execute(select(self.model))
        return list_.scalars().all()

    async def _set_one(self, obj: Base):
        self.session.add(obj)
        # If a user is quick enough, there might be 2 events with the same UUID.
        # There's not much we can do, so simply ignore it until we come up with a better solution
        with suppress(IntegrityError):
            await self.session.commit()
        return True

    async def _delete_all(self):
        await self.session.execute(delete(self.model))
        return True

    async def _delete(self, obj: Base):
        await self.session.delete(obj)
        return True

    async def count(self):
        result = await self.session.execute(select(func.count(self.model.id_)))
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()
        return True
