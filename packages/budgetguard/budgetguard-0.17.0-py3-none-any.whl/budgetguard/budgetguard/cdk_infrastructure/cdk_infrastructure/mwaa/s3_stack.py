from . import constants
from constructs import Construct
from aws_cdk import Stack
from aws_cdk import aws_s3 as _s3


class MWAAS3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        mwaa_bucket = _s3.Bucket(
            self,
            constants.MWAA_BUCKET_NAME,
            bucket_name=constants.MWAA_BUCKET_NAME,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
        )

        self.bucket = mwaa_bucket
