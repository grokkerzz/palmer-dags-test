import os
import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dags import default_args

from core.create_connection_pipeline.tasks import (
    read_pending_connection_task, update_connection_detail)


create_connection_pipeline_every_minute_dag = DAG(
    'create_connection_pipeline_every_minute_dag',
    start_date=datetime.datetime(2019, 8, 21, 8, 20, 2, 84226),
    schedule_interval='*/3 * * * *',
    default_args=default_args,
    catchup=False,
    template_searchpath=os.environ['AIRFLOW_HOME']
)

read_pending_connection_task_operator = PythonOperator(
    task_id='read_pending_connection_task',
    provide_context=True,
    python_callable=read_pending_connection_task,
    dag=create_connection_pipeline_every_minute_dag
)

update_connection_detail_operator = PythonOperator(
    task_id='update_connection_detail',
    provide_context=True,
    python_callable=update_connection_detail,
    dag=create_connection_pipeline_every_minute_dag
)

update_connection_detail_operator.set_upstream(
    read_pending_connection_task_operator)
