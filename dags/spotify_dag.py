from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
# import datetime

from main_using_airflow import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021,9,21),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Our first DAG with ETL process',
    schedule_interval=timedelta(days=1),
)


def just_a_function():
    print("Just testing :)")


run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    # python_callable=just_a_function, # dummy function for testing
    python_callable=run_spotify_etl,
    dag=dag,
)


run_etl