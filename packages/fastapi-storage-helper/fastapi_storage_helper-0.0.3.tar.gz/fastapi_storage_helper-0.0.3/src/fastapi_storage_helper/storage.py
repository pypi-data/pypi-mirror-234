import boto3
from boto.s3.connection import S3Connection
from botocore.config import Config

from config.setting import env


class StorageService:
    def __init__(self, access_key_id: str, secret_key: str, region_name: str):
        self.s3 = boto3.client(
           's3',
           aws_access_key_id=access_key_id,
           aws_secret_access_key=secret_key,
           region_name=region_name,
           config=Config(signature_version='v4'),
        )

        self.s3_v2 = S3Connection(aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

    def create_upload_presign_url(
        self,
        key: str,
        content_length: int,
        content_type: str,
        media_id: str,
        user_id: str,
    ):
        return self.s3.generate_presigned_post(
            env.AWS_S3_BUCKET_NAME,
            key,
            Conditions=[
                {'Content-Type': content_type},
                {'x-amz-meta-id': media_id},
                {'x-amz-meta-user_id': user_id},
                ['content-length-range', 0, content_length],
            ],
            Fields={
                'x-amz-meta-id': media_id,
                'x-amz-meta-user_id': user_id,
                'Content-Type': content_type,
                'bucket': env.AWS_S3_BUCKET_NAME,
            },
            ExpiresIn=1 * 60 * 60,
        )

    # Use boto2 to resolve performance issue
    def create_read_presign_url(self, key: str):
        return self.s3_v2.generate_url(7 * 24 * 60 * 60, 'GET', bucket=env.AWS_S3_BUCKET_NAME, key=key, query_auth=True)

    def get_metadata(self, path: str):
        return self.s3.head_object(Bucket=env.AWS_S3_BUCKET_NAME, Key=path).get('Metadata')
