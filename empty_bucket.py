from app.memes.s3client import s3_client

import asyncio


async def main():
    result = await s3_client.list_objects()
    for i in result["Contents"]:
        name = i["Key"].split("/")[-1]
        await s3_client.delete_file(name)
        print(f"Deleted {name}")


if __name__ == "__main__":
    asyncio.run(main())
