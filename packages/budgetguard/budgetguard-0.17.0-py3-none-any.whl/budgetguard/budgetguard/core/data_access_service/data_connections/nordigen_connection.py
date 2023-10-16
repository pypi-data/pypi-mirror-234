from .aws_connection import AWSConnection
from .connection import Connection
from nordigen import NordigenClient
from nordigen.api import AccountApi
import json
import os
from typing import List, Dict
from loguru import logger


class NordigenConnection(Connection):
    def __init__(self) -> None:
        self.aws_connection: AWSConnection = AWSConnection()
        self.nordigen_json_credentials: Dict[str, str] = json.loads(
            self.aws_connection.get_aws_secret("budget_guard_nordigen_key")
        )
        self.country_code: str = os.environ.get("NORDIGEN_COUNTRY_CODE")
        self.accounts: List[AccountApi] = self.connect()

    def connect(self) -> List[AccountApi]:
        logger.info("Connecting to Nordigen...")
        client = NordigenClient(
            secret_id=self.nordigen_json_credentials["secret_id"],
            secret_key=self.nordigen_json_credentials["secret_key"],
            timeout=99999,
        )
        _ = client.generate_token()  # noqa
        logger.info("Retrieving accounts from Nordigen...")
        accounts = client.requisition.get_requisition_by_id(
            requisition_id=self.nordigen_json_credentials["requisition_id"]
        )
        account_ids = accounts["accounts"]
        account_objects = [
            client.account_api(id=account_id) for account_id in account_ids
        ]
        return account_objects
