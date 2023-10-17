from .aws_connection import AWSConnection  # noqa
from .connection import Connection  # noqa
from .nordigen_connection import NordigenConnection  # noqa
from .s3_connection import S3Connection  # noqa


def connect(connection_name: str) -> Connection:
    """
    Factory function for creating connections.

    :param connection_name: The name of the connection to create.

    :return: The connection.
    """
    if connection_name == "aws":
        return AWSConnection()
    elif connection_name == "s3":
        return S3Connection()
    elif connection_name == "nordigen":
        return NordigenConnection()
    else:
        raise ValueError(f"Connection type {connection_name} not supported.")
