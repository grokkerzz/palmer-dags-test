'''
This file is auto generated from
core/create_task_pipeline/template/embulk/dag.j2
Author: Frank Tran
'''
import os
import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dags import default_args

from core.embulk_task_pipeline.tasks import run_embulk_job


mysql_to_mysql_embulk_task_pipeline_dag = DAG(
    'mysql_to_mysql_dag',
    start_date=datetime.datetime(2019, 8, 21, 8, 20, 2, 84226),
    schedule_interval='*/5 * * * *',
    default_args=default_args,
    catchup=False,
    template_searchpath=os.environ['AIRFLOW_HOME']
)



transaction_sync_operator = PythonOperator(
    task_id='transaction',
    python_callable=run_embulk_job,
    op_kwargs={
        'input_connection_id': '65',
        'output_connection_id': '66',
        'table': 'transaction',
        'has_updated_at': 'False',
        'has_id': 'True',
        'embulk_id': '6'
    },
    dag=mysql_to_mysql_embulk_task_pipeline_dag
)
