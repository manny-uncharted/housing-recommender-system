from modules.selenium_start import webscrape_openrent
from modules.openrent_scraper import openrent_scrape
import pandas
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['housing.recommender@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'openrent_dag',
    default_args=default_args,
    description='Openrent DAG process',
    schedule_interval=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id='complete_openrent_etl',
    python_callable=openrent_scrape,
    dag=dag, 
)

run_etl