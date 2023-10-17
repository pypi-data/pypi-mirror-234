"""Main entrypoint into aws."""
from .s3 import S3, S3Sync

__all__ = ["S3", "S3Sync"]
