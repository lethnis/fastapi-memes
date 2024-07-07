from contextlib import asynccontextmanager
from aiobotocore.session import get_session

from app.config import settings


class S3Storage:
    def __init__(
        self,
        access_key,
        secret_key,
        endpoint_url,
        bucket_name,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }

        self.bucket_name = bucket_name

        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file_locally(self, filepath, filename):
        async with self.get_client() as client:
            with open(filepath, "rb") as f:
                await client.put_object(Bucket=self.bucket_name, Key=filename, Body=f)

    async def upload_file_via_request(self, filename, file):
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=filename, Body=file)

    async def get_file(self, filename):
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=filename)
            return await response["Body"].read()

    async def delete_file(self, filename):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=filename)

    async def paginate(self):
        all_names = []
        async with self.get_client() as client:
            paginator = client.get_paginator("list_objects")
            async for result in paginator.paginate(Bucket=self.bucket_name):
                for c in result.get("Contents", []):
                    all_names.append(c)
            return all_names

    async def list_objects(self):
        # STRANGE THING ONLY FOR THIS FUNCTION
        # REMEMBER FOREVER !!! https://memes.s3.cloud.ru -> https://s3.cloud.ru
        self.config["endpoint_url"] = "https://s3.cloud.ru"
        async with self.session.create_client("s3", **self.config) as client:
            result = await client.list_objects_v2(Bucket=self.bucket_name)
            self.config["endpoint_url"] = "https://memes.s3.cloud.ru"
            return result


s3_storage = S3Storage(
    access_key=settings.ACCESS_KEY,
    secret_key=settings.SECRET_KEY,
    endpoint_url=settings.ENDPOINT_URL,
    bucket_name=settings.BUCKET_NAME,
)
