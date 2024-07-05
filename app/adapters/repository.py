from typing import Literal
from sqlalchemy import select, insert, desc, update, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination.ext.sqlalchemy import paginate

from app.adapters.orm import Memes
from app.domain.entities import Meme


class MemeRepository:

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_memes(self, order_by: Literal["id", "updated_at"] = "id", descending: bool = False):
        return await paginate(
            conn=self.session,
            query=select(Memes).order_by(desc(order_by) if descending else order_by),
        )

    async def add_meme(self, meme: Meme):
        query = (
            insert(Memes)
            .values(filename=meme.filename, description=meme.description, content_type=meme.content_type.value)
            .returning(*Memes.__table__.columns)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.mappings().one()

    async def get_meme_by_id(self, meme_id: int):
        query = select(Memes.__table__.columns).filter_by(id=meme_id)
        result = await self.session.execute(query)
        return result.mappings().one_or_none()

    async def update_meme_by_id(self, meme_id: int, **kwargs):
        # TODO fix kwargs, protect from time changing
        query = (
            update(Memes)
            .filter_by(id=meme_id)
            .values(**kwargs, updated_at=func.now())
            .returning(*Memes.__table__.columns)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.mappings().one_or_none()

    async def delete_meme_by_id(self, meme_id: int):
        query = delete(Memes).filter_by(id=meme_id)
        await self.session.execute(query)
        await self.session.commit()
