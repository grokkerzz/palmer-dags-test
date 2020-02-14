from datetime import timedelta
import requests

from util import logger, NOTIFICATION_EMAILS


def on_success_callback(context):
    logger.info(context)
    logger.info('Success callback')
    # data = { "status": "success" }
    # url = "http://backend.dinovative.com/api/" + type + "/" + task_id
    # r = requests.put(url, data)


def on_failure_callback(context):
    logger.info(context)
    logger.info('Fail callback')
    # data = { "status": "failed" }
    # url = "http://backend.dinovative.com/api/" + context[] + "/" + task_id
    # r = requests.put(url, data)


def on_running_callback(type, task_id):
    data = { "status": "running" }
    url = "http://backend.dinovative.com/api/" + type + "/" + task_id
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
