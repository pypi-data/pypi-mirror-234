from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}


def print_hello():
    print("Hello, Airflow!")


with DAG(
    "test_mwaa_dag", default_args=default_args, schedule_interval=None
) as dag:
    task_hello = PythonOperator(
        task_id="print_hello", python_callable=print_hello
    )
