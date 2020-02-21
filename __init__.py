from datetime import timedelta
import requests

from util import logger, NOTIFICATION_EMAILS


def on_success_callback(context):
    logger.info('Success callback')
    task_id = context['backend_task_id']
    task_type = context['backend_task_type']
    logger.info(context)
    data = { "status": "success" }
    url = "http://backend.dinovative.com/api/" + task_type + "/" + task_id
    r = requests.put(url, data)


def on_failure_callback(context):
    logger.info('Fail callback')
    task_id = context['backend_task_id']
    task_type = context['backend_task_type']
    logger.info(context)
    data = { "status": "failed" }
    url = "http://backend.dinovative.com/api/" + task_type + "/" + task_id
    r = requests.put(url, data)


def on_running_callback(task_type, task_id):
    data = { "status": "running" }
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
