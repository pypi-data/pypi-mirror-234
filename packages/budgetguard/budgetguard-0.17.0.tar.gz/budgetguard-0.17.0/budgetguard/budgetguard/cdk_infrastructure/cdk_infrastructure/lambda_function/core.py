from loguru import logger
import boto3
import json
import re
from typing import Dict, Tuple
import urllib


def lambda_handler(event, context):
    (
        source_bucket,
        source_key,
        partition_id,
        account_id,
        data_type,
    ) = get_ingestion_details(event)
    formatter = Formatter(data_type)
    destination_bucket = "budget-guard-bronze"
    destination_key = f"{data_type}/partition_id={partition_id}/account_id={account_id}/{source_key.split('/')[-1]}"  # noqa
    data = s3_read_json(source_bucket, source_key)
    data = formatter(data)
    s3_write_json(data, destination_bucket, destination_key)
    logger.info(
        "Successfully copied data from {0} to {1}!".format(
            source_bucket, destination_bucket
        )
    )


def get_ingestion_details(event: Dict) -> Tuple[str, str, str, str, str]:
    """
    Method for getting the details of the ingestion event.
    """

    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = urllib.parse.unquote(
        event["Records"][0]["s3"]["object"]["key"]
    )
    logger.info(
        "Received event from {0} for {1}.".format(source_bucket, source_key)
    )  # noqa
    partition_id = re.search(r"partition_id=(\d+)", source_key).group(1)
    account_id = re.search(r"account_id=([a-zA-Z0-9-]+)", source_key).group(1)
    data_type = source_key.split("/")[0]
    logger.info(
        "Received event from {0} for {1} data in partition {2} for account {3}.".format(  # noqa
            source_bucket, data_type, partition_id, account_id
        )
    )

    return source_bucket, source_key, partition_id, account_id, data_type


def s3_read_json(source_bucket: str, source_key: str) -> Dict:
    """
    Method for reading a JSON file from S3.
    """

    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        logger.info("Reading JSON data from {0}...".format(source_bucket))
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        json_data = response["Body"].read().decode("utf-8")
        parsed_data = json.loads(json_data)
        return parsed_data

    except Exception as e:
        print("Error: {}".format(str(e)))
        return {"statusCode": 500, "body": "Error: {}".format(str(e))}


def s3_write_json(json_data: str, target_bucket: str, target_key: str) -> Dict:
    """
    Method for writing a JSON file to S3.
    """

    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        logger.info("Writing JSON data to {0}...".format(target_bucket))
        response = s3.put_object(
            Bucket=target_bucket, Key=target_key, Body=json.dumps(json_data)
        )

        return response

    except Exception as e:
        print("Error: {}".format(str(e)))
        return {"statusCode": 500, "body": "Error: {}".format(str(e))}


class Formatter:
    def __init__(self, data_type: str):
        self.data_type = data_type

    def __call__(self, data: Dict) -> Dict:
        return self.get_nordigen_function(self.data_type)(data)

    @staticmethod
    def camel_to_snake(s: str) -> str:
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def get_nordigen_function(self, data_type: str):
        if data_type == "balances":
            return self.format_balances
        elif data_type == "transactions":
            return self.format_transactions
        elif data_type == "details":
            return self.format_details
        elif data_type == "metadata":
            return self.format_metadata
        else:
            raise ValueError("Invalid data type specified!")

    def format_transactions(self, transactions):
        transactions_flatten = []
        logger.info("Flattening transactions...")
        for transaction_status, transactions_info in transactions[
            "transactions"
        ].items():
            logger.info(
                "Flattening transactions for status {0}...".format(
                    transaction_status
                )  # noqa
            )
            logger.info(
                "Number of transactions with status {0}: {1}".format(
                    transaction_status, len(transactions_info)
                )
            )
            for transaction in transactions_info:
                transaction["transactionStatus"] = transaction_status
                transaction["transactionCurrency"] = transaction[
                    "transactionAmount"
                ]["currency"]
                transaction["transactionAmount"] = transaction[
                    "transactionAmount"
                ]["amount"]
                if transaction.get("debtorAccount"):
                    transaction["debtorAccountIban"] = transaction[
                        "debtorAccount"
                    ]["iban"]
                    del transaction["debtorAccount"]
                else:
                    transaction["creditorAccountIban"] = transaction[
                        "creditorAccount"
                    ]["iban"]
                    del transaction["creditorAccount"]
                transaction["balanceAfterTransactionAmount"] = transaction[
                    "balanceAfterTransaction"
                ]["balanceAmount"]["amount"]
                transaction["balanceAfterTransactionCurrency"] = transaction[
                    "balanceAfterTransaction"
                ]["balanceAmount"]["currency"]
                del transaction["remittanceInformationUnstructured"]
                del transaction["balanceAfterTransaction"]
                transactions_flatten.append(
                    {self.camel_to_snake(k): v for k, v in transaction.items()}
                )
        logger.info("Finished flattening transactions!")
        return transactions_flatten

    def format_balances(self, balances):
        balances_flattened = balances.get("balances", {})
        balances_flattened = [
            {
                "balanceAmount": balance.get("balanceAmount", {}).get(
                    "amount", ""
                ),
                "balanceCurrency": balance.get("balanceAmount", {}).get(
                    "currency", ""
                ),
                "balanceType": balance.get("balanceType", ""),
            }
            for balance in balances_flattened
        ]
        balances_flattened = [
            {self.camel_to_snake(key): value for key, value in balance.items()}
            for balance in balances_flattened
        ]
        return balances_flattened

    def format_details(self, details):
        details_flattened = details.get("account", {})
        details_flattened = {
            self.camel_to_snake(k): v for k, v in details_flattened.items()
        }
        return details_flattened

    def format_metadata(self, metadata):
        return metadata
