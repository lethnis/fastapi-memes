import asyncio
import os
from uuid import uuid4
import re

from app.memes.service import MemesService
from app.memes.s3client import s3_client


async def upload_memes(filename, filepath):
    filename = re.sub("[\s\(\)]+", "-", filename)
    filename = f"{uuid4()}-{filename}"
    await s3_client.upload_file_locally(filepath, filename)
    await MemesService.add_meme(filename)


async def main():
    for i in os.listdir("my_memes"):
        filepath = os.path.join("my_memes", i)
        await upload_memes(i, filepath)
        print(f"Uploaded {i}")


if __name__ == "__main__":
    asyncio.run(main())
