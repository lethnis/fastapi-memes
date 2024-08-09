import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from aiobotocore.session import get_session

from app.config import settings


class MemeStorage:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
        policy_file: str = "policy.json",
    ):
        """Connection to the S3 storage. Can put, delete and get files.

        Args:
            access_key (str): access key for storage. If use minio provide MINIO_ROOT_USER.
            secret_key (str): secret key for storage. If use minio provide MINIO_ROOT_PASSWORD.
            endpoint_url (str): url for the API. If use minio it is probably the default value - localhost:9000.
            bucket_name (str): bucket name to store files.
            policy_file (str, optional): policy file for custom policies. Defaults to "policy.json".
        """

        # init configs for the session
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }

        self.bucket_name = bucket_name

        self.session = get_session()

        # create bucket if it does not exist
        if not asyncio.run(self.bucket_exists()):
            asyncio.run(self.create_bucket())

        # add policy if it does not exist
        if not asyncio.run(self.get_policy()):
            asyncio.run(self.add_policy(policy_file))

        logging.info("All set!")

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_local_file(self, filepath: str, filename: str | None = None) -> None:
        """Upload local file from disk.

        Args:
            filepath (str): path to a file.
            filename (str | None, optional): file name. If not provided will be set to it's name in filepath. Defaults to None.
        """

        if not filename:
            filename = Path(filepath).name

        async with self.get_client() as client:
            with open(filepath, "rb") as f:
                await client.put_object(Bucket=self.bucket_name, Key=filename, Body=f)

    async def upload_file_via_request(self, filename: str, file: bytes):
        """Upload file via request form from FastAPI.

        Args:
            filename (str): filename.
            file (bytes): file in bytes.
        """
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=filename, Body=file)

    async def get_file(self, filename: str) -> bytes:
        """Get raw file in bytes.

        Args:
            filename (str): name of the file in the storage.

        Returns:
            bytes: file
        """
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=filename)
            return await response["Body"].read()

    async def get_file_url(self, filename: str) -> str:
        """Generates url for a file. File will be accessible from a browser, if a proper policy is set.

        Args:
            filename (str): name of the file in the storage.

        Returns:
            str: url string
        """
        return f"{self.config['endpoint_url']}/{self.bucket_name}/{filename}"

    async def delete_file(self, filename: str) -> None:
        """Deletes a file from a bucket.

        Args:
            filename (str): name of the file in the storage.
        """
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=filename)

    async def add_policy(self, policy_file: str) -> None:
        """Add policy to the bucket.

        Args:
            policy_file (str): proper policy.json file.
        """
        async with self.get_client() as client:
            try:
                await client.put_bucket_policy(Bucket=self.bucket_name, Policy=open(policy_file).read())
                logging.info(f"Added policy for bucket '{self.bucket_name}'")
            except (FileNotFoundError, TypeError):
                logging.warn(f"Could not open policy file '{policy_file}'")

    async def get_policy(self) -> str | None:
        """Get policy for the bucket.

        Returns:
            str | None: policy content if any.
        """
        async with self.get_client() as client:
            try:
                return await client.get_bucket_policy(Bucket=self.bucket_name)
            except client.exceptions.ClientError:
                logging.info(f"No policy for bucket '{self.bucket_name}'")

    async def delete_policy(self) -> None:
        """Deletes policy for the bucket if possible."""
        if await self.get_policy():
            async with self.get_client() as client:
                await client.delete_bucket_policy(Bucket=self.bucket_name)
                logging.info(f"Deleted policy for bucket '{self.bucket_name}'")

    async def bucket_exists(self) -> bool:
        """Check if bucket exists.

        Returns:
            bool: True if exists.
        """
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket_name)
                return True
            except client.exceptions.ClientError:
                return False

    async def create_bucket(self) -> None:
        """Creates the bucket."""
        async with self.get_client() as client:
            try:
                await client.create_bucket(Bucket=self.bucket_name)
                logging.info(f"Created bucket {self.bucket_name}")
            except client.exceptions.BucketAlreadyOwnedByYou:
                logging.info(f"Bucket '{self.bucket_name}' already exists.")

    async def delete_bucket(self) -> None:
        """Deletes the bucket."""
        async with self.get_client() as client:
            try:
                await client.delete_bucket(Bucket=self.bucket_name)
                logging.info(f"Deleted bucket {self.bucket_name}")
            except client.exceptions.NoSuchBucket:
                logging.info(f"Bucket '{self.bucket_name}' does not exist.")

    async def list_files(self) -> list[dict]:
        """List all files in the bucket."""
        async with self.get_client() as client:
            return (await client.list_objects_v2(Bucket=self.bucket_name))["Contents"]


s3_storage = MemeStorage(
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    endpoint_url=settings.ENDPOINT_URL,
    bucket_name=settings.BUCKET_NAME,
)
