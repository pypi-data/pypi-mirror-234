import boto3
from botocore.exceptions import ClientError
from .connection import Connection
import os
from loguru import logger


class AWSConnection(Connection):
    def __init__(self) -> None:
        self.session: boto3.session.Session = AWSConnection.connect(self)

    def connect(self) -> boto3.session.Session:
        """
        Base method for connecting to the data source.

        :return: The session object.
        """
        logger.info("Connecting to AWS session...")
        session = boto3.session.Session(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION_NAME"),
        )
        return session

    def get_aws_secret(self, secret_name: str) -> str:
        """
        Method to retrieve a secret from AWS Secrets Manager.

        :param secret_name: The name of the secret to retrieve.

        :return: The secret value.
        """
        client: boto3.client = self.session.client(
            service_name="secretsmanager",
        )
        logger.info(
            f"Retrieving secret {secret_name} from AWS Secrets Manager..."  # noqa
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response["SecretString"]
        return secret
