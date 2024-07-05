import re
from typing import Annotated, Literal
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi_pagination.links import Page

from app.memes.schemas import MemesResponse
from app.memes.service import MemesService
from app.memes.s3client import s3_client

router = APIRouter(prefix="/memes", tags=["Мемы"])


@router.get("", response_model=Page[MemesResponse])
async def get_memes(order_by: Literal["id", "updated_at"] = "id", descending: bool = False):
    return await MemesService.get_memes(order_by, descending)


@router.post("", response_model=MemesResponse)
async def upload_meme(file: UploadFile, description: str | None = None):
    filename = re.sub("[\s\(\)]+", "-", file.filename)
    filename = f"{uuid4()}-{filename}"
    await s3_client.upload_file_via_request(filename, file.file)
    result = await MemesService.add_meme(filename, description)
    return result


@router.get("/{id}", response_model=MemesResponse)
async def get_meme_by_id(meme_id: int):
    return await MemesService.get_meme_by_id(meme_id)


# TODO make file optional!!!
@router.put("/{id}", response_model=MemesResponse)
async def update_meme(id: int, file: UploadFile = None, description: str | None = None):

    kwargs = {}

    if not file and not description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if file:
        old_filename = (await MemesService.get_meme_by_id(id))["filename"]
        await s3_client.delete_file(old_filename)
        new_filename = f"{uuid4()}-{file.filename}"
        await s3_client.upload_file_via_request(new_filename, file.file)
        kwargs["filename"] = new_filename

    if description:
        kwargs["description"] = description

    return await MemesService.update_meme_by_id(id, **kwargs)


# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meme(id: int):
    filename = (await MemesService.get_meme_by_id(id))["filename"]
    await s3_client.delete_file(filename)
    await MemesService.delete_meme_by_id(id)
