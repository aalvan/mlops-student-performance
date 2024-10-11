from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.decorators import task_group

from datetime import datetime, timedelta

default_args = {
    'owner': 'Código Facilito Team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry': False,
    'retry_delay': False,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    'test_dag_dummy',
    start_date = None,
    default_args = default_args,
    schedule_interval = None,
    description = "A test pipeline",
    tags = ['mlops']
    ) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> end