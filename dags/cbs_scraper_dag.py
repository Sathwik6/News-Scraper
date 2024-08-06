from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cbs_scraper_dag',
    default_args=default_args,
    description='A simple DAG to run the CBS scraper',
    schedule_interval=timedelta(hours=1),
    catchup=False,  # Ensure no backfill occurs
)

def run_scraper():
    scraper_path = os.path.join(os.environ['AIRFLOW_HOME'], 'scraper', 'scraper.py')
    logging.info(f"Running scraper: {scraper_path}")
    result = subprocess.run(['python3', scraper_path], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Scraper failed: {result.stderr}")
        raise Exception(f"Scraper failed: {result.stderr}")
    logging.info(result.stdout)

run_scraper_task = PythonOperator(
    task_id='run_cbs_scraper',
    python_callable=run_scraper,
    dag=dag,
)

run_scraper_task
