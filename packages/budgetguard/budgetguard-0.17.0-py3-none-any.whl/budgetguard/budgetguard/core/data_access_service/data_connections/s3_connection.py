from .aws_connection import AWSConnection
import os
import boto3


class S3Connection(AWSConnection):
    def __init__(self) -> None:
        super().__init__()
        self.s3_client: boto3.client = self.connect()

    def connect(self) -> boto3.client:
        """
        Method to retrieve an S3 client.

        :return: The S3 client.
        """
        client: boto3.client = self.session.client(
            service_name="s3",
            region_name=os.environ.get("AWS_REGION_NAME"),
        )
        return client
