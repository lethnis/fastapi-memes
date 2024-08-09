from typing import Literal
from sqlalchemy import select, insert, desc, update, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.orm import MemesTable
from app.domain.entities import Meme


class SQLAlchemyRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_memes(
        self,
        order_by: Literal["id", "updated_at"] = "id",
        descending: bool = False,
        offset=0,
        limit=10,
    ) -> list[MemesTable]:

        query = (
            select(MemesTable.__table__.columns)
            .order_by(desc(order_by) if descending else order_by)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.mappings().all()

    async def get_meme_by_id(self, meme_id: int) -> MemesTable | None:
        query = select(MemesTable.__table__.columns).filter_by(id=meme_id)
        result = await self.session.execute(query)
        return result.mappings().one_or_none()

    async def add_meme(self, meme: Meme) -> type[MemesTable]:
        query = (
            insert(MemesTable)
            .values(filename=meme.filename, description=meme.description, content_type=meme.content_type.value)
            .returning(*MemesTable.__table__.columns)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.mappings().one()

    async def update_meme_by_id(self, meme_id: int, **kwargs) -> MemesTable | None:

        if any(i in kwargs.keys() for i in ("updated_at", "created_at", "id", "content_type")):
            raise ValueError("Can't update provided fields.")

        query = (
            update(MemesTable)
            .filter_by(id=meme_id)
            .values(**kwargs, updated_at=func.now())
            .returning(*MemesTable.__table__.columns)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.mappings().one_or_none()

    async def delete_meme_by_id(self, meme_id: int) -> None:
        query = delete(MemesTable).filter_by(id=meme_id)
        await self.session.execute(query)
        await self.session.commit()
