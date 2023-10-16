from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from budgetguard.main import run

default_args = {
    "owner": "budget-guard",
    "start_date": datetime(2023, 8, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

PARTITION_ID = "{{ yesterday_ds_nodash }}"
TASK_ID = "ingest_account_data"
# Daily at 1am
SCHEDULE_INTERVAL = "0 1 * * *"

with DAG(
    "ingest_account_data_dag",
    default_args=default_args,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,
    max_active_runs=1,
    concurrency=1,
) as dag:
    start = EmptyOperator(task_id="start")
    ingest_account_data = PythonOperator(
        task_id=TASK_ID,
        python_callable=run,
        op_kwargs={"task": TASK_ID, "partition_id": PARTITION_ID},
    )
    end = EmptyOperator(task_id="end")

    start >> ingest_account_data >> end
