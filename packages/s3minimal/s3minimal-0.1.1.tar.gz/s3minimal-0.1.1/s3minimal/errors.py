class BaseError(Exception):
    pass


class UploadError(BaseError):
    pass


class DownloadError(BaseError):
    pass


class MoveError(BaseError):
    pass


class GeneratePresignedUrlError(BaseError):
    pass


class CreateBucketError(BaseError):
    pass
