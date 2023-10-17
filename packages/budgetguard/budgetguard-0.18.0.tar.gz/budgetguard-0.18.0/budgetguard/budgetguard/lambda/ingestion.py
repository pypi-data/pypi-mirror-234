from budgetguard.main import run
from datetime import datetime


def lambda_handler(event, context):
    task = "ingest_account_data"
    partition_id = datetime.now().strftime("%Y%m%d")
    run(task, partition_id)
