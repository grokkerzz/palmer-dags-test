from datetime import timedelta
import requests

from util import logger, NOTIFICATION_EMAILS


def on_success_callback(context):
    logger.info('Success callback')
    logger.info(context)
    task_instance = context['task_instance']
    backend_update_status = task_instance.xcom_pull(task_ids='running_update_status', key='backend_update_status')
    data = { "status": "success" }
    url = "http://backend.dinovative.com/api/" + backend_update_status
    r = requests.put(url, data)


def on_failure_callback(context):
    logger.info('Fail callback')
    logger.info(context)
    task_instance = context['task_instance']
    backend_update_status = task_instance.xcom_pull(task_ids='running_update_status', key='backend_update_status')
    data = { "status": "failed" }
    url = "http://backend.dinovative.com/api/" + backend_update_status
    r = requests.put(url, data)


def on_running_callback(task_type, task_id, **context):
    task_instance = context['task_instance']
    backend_update_status = task_type + "/" + task_id
    task_instance.xcom_push(key='backend_update_status', value=backend_update_status)
    data = { "status": "running" }
    url = "http://backend.dinovative.com/api/" + backend_update_status
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
