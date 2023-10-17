import io
import os
import asyncio
from aiobotocore.session import get_session, AioSession
from botocore.exceptions import ClientError
from s3minimal.errors import *

HOUR = 60 * 60
DAY = HOUR * 24


class S3:
    session: AioSession
    bucket: str
    endpoint_url: str
    region_name: str
    aws_access_key_id: str
    aws_secret_access_key: str

    def __init__(
        self,
        endpoint_url: str,
        region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket: str = None,
    ):
        """
        Initializes S3.
        # Example:
        >>> s3 = S3(
        ...     endpoint_url="https://s3.amazonaws.com",
        ...     region_name="us-east-1",
        ...     aws_access_key_id="access_key",
        ...     aws_secret_access_key="secret_key",
        ... )
        """
        self.session = get_session()
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.set_bucket(bucket)

    def set_bucket(self, bucket: str) -> None:
        """
        Sets the bucket to be used for S3.
        # Example:
        >>> set_bucket("bucket_name")
        None
        """
        self.bucket = bucket

    async def __get_client(self):
        """
        Gets a client for S3. This is a private method.
        """
        return self.session.create_client(
            "s3",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    async def download(self, key: str) -> io.BytesIO:
        """
        Downloads a file from S3.
        # Example:
        >>> download("bucket/OCR/FileName.pdf")
        <_io.BytesIO object at 0x7f7f7f7f7f7f>
        """
        async with await self.__get_client() as client:
            try:
                obj = await client.get_object(Bucket=self.bucket, Key=key)
                file_contents = await obj["Body"].read()
                return io.BytesIO(file_contents)
            except Exception:
                raise DownloadError(f"Failed to download {key}")

    async def upload(
        self,
        key: str,
        file_obj: io.BytesIO,
    ) -> None:
        """
        Uploads a file to S3.
        # Example:
        >>> upload("bucket/OCR/FileName.pdf", file_obj)
        None
        """
        async with await self.__get_client() as client:
            try:
                await client.put_object(Bucket=self.bucket, Key=key, Body=file_obj)
            except Exception:
                raise UploadError(f"Failed to upload {key}")

    async def move(self, src: str, dest: str) -> bool:
        """
        Moves a file from `src` to `dest` in S3.
        # Example:
        >>> move("bucket/OCR/FileName.pdf", "bucket/OCR/FileName.pdf/subfolder")
        True
        >>> move("path/to/nofile", "bucket/OCR/FileName.pdf/subfolder")
        False
        """
        try:
            async with await self.__get_client() as client:
                await client.copy_object(
                    Bucket=self.bucket,
                    CopySource={"Bucket": self.bucket, "Key": src},
                    Key=dest,
                )
                await client.delete_object(Bucket=self.bucket, Key=src)
        except Exception:
            raise MoveError(f"Failed to move {src} to {dest}")

    async def generate_presigned_url(self, key: str, expires_in: int = DAY) -> str:
        """
        Generates a presigned url for S3.
        # Example:
        >>> generate_presigned_url("bucket/OCR/FileName.pdf")
        "https://bucket.s3.amazonaws.com/OCR/FileName.pdf?AWSAccessKeyId=..."
        """
        async with await self.__get_client() as client:
            try:
                return await client.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={"Bucket": self.bucket, "Key": key},
                    ExpiresIn=expires_in,
                )
            except Exception:
                raise GeneratePresignedUrlError(f"Failed to generate presigned url")

    async def create_bucket(self, bucket_name: str, **kwargs) -> None:
        """
        Creates a bucket in S3.
        # Example:
        >>> create_bucket("bucket_name")
        None
        """
        async with await self.__get_client() as client:
            try:
                await client.create_bucket(Bucket=bucket_name)

                set_cors = kwargs.get("set_cors", False)

                if set_cors:
                    cors_configuration = kwargs.get("cors_configuration", {})
                    await client.put_bucket_cors(
                        Bucket=bucket_name,
                        CORSConfiguration=cors_configuration,
                    )
            except ClientError as e:
                raise CreateBucketError(f"Failed to create bucket {bucket_name}: {e}")

    async def list_files(self, path: str) -> list:
        """
        Lists files in a path in S3.
        # Example:
        >>> list_files("bucket/OCR/")
        [
            {
                "Key": "bucket/OCR/FileName.pdf",
                "LastModified": datetime.datetime(2021, 1, 1, 0, 0, tzinfo=tzutc()),
                "ETag": '"etag"',
                "Size": 123,
                "StorageClass": "STANDARD",
                "Owner": {
                    "DisplayName": "owner",
                    "ID": "owner_id"
                }
            },
            ...
        ]
        """
        async with await self.__get_client() as client:
            try:
                response = await client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=path,
                )
                return response["Contents"]
            except Exception:
                raise DownloadError(f"Failed to list files in {path}")

    @staticmethod
    def create_key(*args, **kwargs) -> str:
        """
        Creates a key for S3. Order of arguments matters.
        # Example:
        >>> create_key("bucket", "OCR", "FileName.pdf")
        "bucket/OCR/FileName.pdf"
        >>> create_key("bucket", "OCR", "FileName.pdf", "subfolder")
        "bucket/OCR/FileName.pdf/subfolder"
        """
        return os.path.join(*args, **kwargs)


class S3Sync(S3):
    """
    Synchronous version of S3.
    """

    def download(self, key: str) -> io.BytesIO:
        return asyncio.run(super().download(key))

    def upload(self, key: str, file_obj: io.BytesIO) -> None:
        return asyncio.run(super().upload(key, file_obj))

    def move(self, src: str, dest: str) -> bool:
        return asyncio.run(super().move(src, dest))

    def generate_presigned_url(self, key: str, expires_in: int = DAY) -> str:
        return asyncio.run(super().generate_presigned_url(key, expires_in))

    def create_bucket(self, bucket_name: str, **kwargs) -> None:
        return asyncio.run(super().create_bucket(bucket_name, **kwargs))

    def list_files(self, path: str) -> list:
        return asyncio.run(super().list_files(path))
