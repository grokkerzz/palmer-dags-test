import os
import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dags import default_args

from core.create_task_pipeline.tasks import (
    read_pending_embulk_task, read_pending_sql_task,
    create_embulk_task, create_sql_task)


create_task_pipeline_dag = DAG(
    'create_task_pipeline_dag',
    start_date=datetime.datetime(2019, 8, 21, 8, 20, 2, 84226),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    template_searchpath=os.environ['AIRFLOW_HOME']
)

read_pending_embulk_task_operator = PythonOperator(
    task_id='read_pending_embulk_task',
    provide_context=True,
    python_callable=read_pending_embulk_task,
    dag=create_task_pipeline_dag
)

read_pending_sql_task_operator = PythonOperator(
    task_id='read_pending_sql_task',
    provide_context=True,
    python_callable=read_pending_sql_task,
    dag=create_task_pipeline_dag
)

create_embulk_task_operator = PythonOperator(
    task_id='create_embulk_task',
    provide_context=True,
    python_callable=create_embulk_task,
    dag=create_task_pipeline_dag
)

create_sql_task_operator = PythonOperator(
    task_id='create_sql_task',
    provide_context=True,
    python_callable=create_sql_task,
    dag=create_task_pipeline_dag
)


create_embulk_task_operator.set_upstream(read_pending_embulk_task_operator)
create_sql_task_operator.set_upstream(read_pending_sql_task_operator)
