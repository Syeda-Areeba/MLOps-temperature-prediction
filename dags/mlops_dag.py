from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.abspath('/opt/airflow/DVC/scripts'))

from fetch_data import fetch_weather_data
from extract_data import extract_weather_data_to_csv
from preprocess_data import preprocess_and_save

def end_msg():
    print("Ended!")

def dvc_add():
    os.chdir('/opt/airflow/DVC') 
    os.system('dvc add data/raw_weather_data.json data/raw_weather_data.csv data/processed_weather_data.csv')

def dvc_push():
    os.chdir('/opt/airflow/DVC')  
    os.system('dvc push') 

def dvc_repro():
    os.chdir('/opt/airflow/DVC')  
    os.system('dvc repro')

with DAG("mlops_dag", start_date=datetime(2024, 1, 1), schedule_interval="@hourly", catchup=False) as dag:

    task_1 = PythonOperator(
        task_id='Fetching_Data',
        execution_timeout=timedelta(minutes=10),
        retries=3,
        python_callable=fetch_weather_data,
    )

    task_2 = PythonOperator(
        task_id='Extracting_Data',
        execution_timeout=timedelta(minutes=10),
        retries=3,
        python_callable=extract_weather_data_to_csv,
    )

    task_3 = PythonOperator(
        task_id='Preprocessing_Data',
        execution_timeout=timedelta(minutes=10),
        retries=3,
        python_callable=preprocess_and_save,
    )

    # task_4 = BashOperator(
    #     task_id='Change_dir',
    #     bash_command='cd /opt/airflow/DVC && cd .dvc',
    #     retries=3,
    #     execution_timeout=timedelta(minutes=15),
    # )

    # task_5 = BashOperator(
    #     task_id='Show_dir',
    #     bash_command='pwd',
    #     retries=3,
    #     execution_timeout=timedelta(minutes=15),
    # )

    task_4 = PythonOperator(
        task_id='DVC_repro',
        python_callable=dvc_repro,
        retries=3,
        execution_timeout=timedelta(minutes=15),
    )

    task_5 = PythonOperator(
        task_id='DVC_Add',
        python_callable=dvc_add,
        retries=3,
        execution_timeout=timedelta(minutes=15),
    )

    task_6 = PythonOperator(
        task_id='Push_to_DVC',
        python_callable=dvc_push,
        retries=3,
        execution_timeout=timedelta(minutes=15),
    )

    task_7 = PythonOperator(
        task_id='End_Msg',
        execution_timeout=timedelta(minutes=10),
        retries=3,
        python_callable=end_msg,
    )

    task_1 >> task_2 >> task_3 >> task_4 >> task_5 >> task_6 >> task_7