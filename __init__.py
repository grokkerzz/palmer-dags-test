from datetime import timedelta
import requests

from util import logger, NOTIFICATION_EMAILS


def on_success_callback(**context):
    logger.info('Success callback')
    logger.info(context)
    logger.info(task_instance.xcom_pull(task_ids='running_update_status'))
    task_instance = context['task_instance']
    task_id = task_instance.xcom_pull(task_ids='running_update_status', key='backend_task_id')
    task_type = task_instance.xcom_pull(task_ids='running_update_status' key='backend_task_type')
    data = { "status": "success" }
    url = "http://backend.dinovative.com/api/" + task_type + "/" + task_id
    r = requests.put(url, data)


def on_failure_callback(**context):
    logger.info('Fail callback')
    logger.info(context)
    task_instance = context['task_instance']
    task_id = task_instance.xcom_pull(task_ids='running_update_status', key='backend_task_id')
    task_type = task_instance.xcom_pull(task_ids='running_update_status' key='backend_task_type')
    data = { "status": "failed" }
    url = "http://backend.dinovative.com/api/" + task_type + "/" + task_id
    r = requests.put(url, data)


def on_running_callback(task_type, task_id, **context):
    data = { "status": "running" }
    task_instance = context['task_instance']
    task_instance.xcom_push(key='backend_task_id', value=task_id)
    task_instance.xcom_push(key='backend_task_type', value=task_type)
    url = "http://backend.dinovative.com/api/" + task_type + "/" + task_id
    r = requests.put(url, data)


default_args = {
    'owner': 'palmer',
    'depends_on_past': False,
    'on_failure_callback': on_failure_callback,
    'on_success_callback': on_success_callback,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'email': NOTIFICATION_EMAILS,
    'email_on_failure': True,
    'email_on_retry': False,
}


default_system_args = {
    'owner': 'palmer',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'email': NOTIFICATION_EMAILS,
    'email_on_failure': True,
    'email_on_retry': False,
}
