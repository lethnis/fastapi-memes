import pytest
from app.repository.repository import SQLAlchemyRepository

from app.repository.orm import async_session


@pytest.mark.asyncio
async def test_get_memes():
    async with async_session() as session:
        meme_repo = SQLAlchemyRepository(session)
        result = await meme_repo.get_memes()
        assert result is not None


# @pytest.mark.asyncio
# async def test_get_meme_by_id():
#     async with async_session() as session:
#         meme_repo = SQLAlchemyRepository(session)
#         result = await meme_repo.get_meme_by_id(4)
#         assert result is not None


# @pytest.mark.asyncio
# async def test_get_meme_by_id_not_exist():
#     async with async_session() as session:
#         meme_repo = SQLAlchemyRepository(session)
#         result = await meme_repo.get_meme_by_id(9999)
#         assert result is None
