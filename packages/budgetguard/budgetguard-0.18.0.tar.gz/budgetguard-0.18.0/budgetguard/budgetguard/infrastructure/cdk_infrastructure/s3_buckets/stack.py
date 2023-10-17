from aws_cdk import Stack
from aws_cdk import aws_s3 as _s3
from constructs import Construct


class S3DeployStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, bucket_id: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.create_bucket(bucket_id)

    def create_bucket(self, bucket_id: str):
        _s3.Bucket(
            self,
            bucket_id,
            bucket_name=bucket_id,
        )
