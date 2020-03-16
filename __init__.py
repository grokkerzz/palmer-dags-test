from datetime import timedelta

from util import logger, NOTIFICATION_EMAILS


def on_success_callback(context):
    logger.info('Success callback')
    logger.info(context)


def on_failure_callback(context):
    logger.info('Fail callback')
    logger.info(context)


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
