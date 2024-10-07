from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime, timedelta


default_args = {
    'owner': 'Alexis Alva',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry': False,
}

@task.virtualenv(
    requirements = ["mlflow"],
    venv_cache_path="/tmp/venv_cache"
)
def _test_mlflow():
    import mlflow
    
    TRACKING_SERVER_HOST = "mlflow_server"
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    mlflow.set_experiment("student_performance")

    mlflow.set_experiment_tags(
        {
        "project" : "Student Performance",
        "task": "Regression"
        }
    )
    print(f"tracking URI: {mlflow.get_tracking_uri()}")
    


with DAG(
    'student_performance',
    start_date = None,
    default_args = default_args,
    schedule_interval = None,
    description = "A ML pipeline for student performance",
    tags = ['mlops']
) as dag:
    
    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    start >> _test_mlflow() >> end