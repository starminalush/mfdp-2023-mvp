# flake8: noqa: WPS117
"""Custom S3 client for boto3."""
import io
from os import getenv

import aioboto3


class S3Client:

    def __init__(self):
        self._session = None
        self._client = None
        self._bucket_name = getenv("BUCKET")

    async def _close(self):
        if self._client is not None:
            await self._client.close()

        if self._session is not None:
            await self._session.close()

    async def __aenter__(self):
        return await S3Client._create()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._close()

    @classmethod
    async def _create(cls) -> 'S3Client':
        """Create instance of S3Client.

        Returns:
            Instance of S3Client.
        """
        self = cls()
        if not self._client:
            if not self._session:
                self._session = aioboto3.Session()
            self._client = self._session.client(
                service_name="s3",
                endpoint_url=getenv("S3_ENDPOINT_URL"),
                aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self

    async def upload_file(self, filename: str, img_bytes: bytes):
        """Upload image to s3.

        Args:
            filename: Path in minio.
            img_bytes: Input image.
        """
        async with self._client as client:
            await client.upload_fileobj(
                io.BytesIO(img_bytes),
                Bucket=self._bucket_name,
                Key=filename,
            )
