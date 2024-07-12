from fastapi import APIRouter

from app.service.meme import MemeService
from app.domain.entities import Meme

app = APIRouter("/memes", tags=["Мемы"])


@app.get("/{id}")
async def get_meme_by_id(id: int):
    await MemeService.get_by_id(id)


@app.get("")
async def get_memes(limit: int, offset: int):
    await MemeService.get_all(limit, offset)


@app.post("")
async def add_meme(meme: Meme):
    await MemeService.add(meme)


@app.put("")
async def replace_meme(meme: Meme):
    await MemeService.replace(meme)


@app.patch("")
async def update_meme(meme: Meme):
    await MemeService.update(meme)


@app.delete("/{id}")
async def delete_meme(id: int):
    await MemeService.delete(id)
