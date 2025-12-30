import os

import boto3

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET", "handled")

session = boto3.session.Session()
client = session.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)


def upload_file(file_path: str, key: str) -> str:
    client.upload_file(file_path, S3_BUCKET, key)
    return f"{S3_BUCKET}/{key}"
