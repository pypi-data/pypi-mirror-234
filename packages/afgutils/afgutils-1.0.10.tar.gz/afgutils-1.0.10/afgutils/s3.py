import boto3
from os import getenv as _getenv
from io import BytesIO


def save_to_s3(s3_key: str, content_body: str, aws_access_key_id=None,
               aws_secret_access_key=None, aws_region=None, s3_bucket=None):
    s3_client = _get_s3_client(aws_access_key_id, aws_secret_access_key, aws_region)
    s3_bucket = s3_bucket or _getenv('s3_bucket_risk')

    s3_client.put_object(Bucket=s3_bucket
                         , Body=content_body
                         , Key=s3_key
                         )


def get_from_s3(s3_key, filename: str = None, aws_access_key_id=None,
                aws_secret_access_key=None, aws_region=None, s3_bucket=None, as_bytes: bool = False):
    s3_client = _get_s3_client(aws_access_key_id, aws_secret_access_key, aws_region)
    s3_bucket = s3_bucket or _getenv('s3_bucket_lms')

    if as_bytes:
        with BytesIO() as f:
            s3_client.download_fileobj(s3_bucket, s3_key, f)
            return f.getvalue()

    s3_client.download_file(
        Bucket=s3_bucket,
        Key=s3_key,
        Filename=filename
    )


def _get_s3_client(aws_access_key_id=None, aws_secret_access_key=None, aws_region=None):
    aws_access_key_id = aws_access_key_id or _getenv('aws_access_key_id')
    aws_secret_access_key = aws_secret_access_key or _getenv('aws_secret_access_key')
    aws_region = aws_region or _getenv('aws_region_name')
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
