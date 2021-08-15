# celery / django imports
from celery.decorators import task
from celery.utils.log import get_task_logger

# custom imports
from .email import send_review_email


logger = get_task_logger(__name__)


@task(name="send_review_email_task")
def send_review_email_task(name, email, review):
    logger.info("Sent email")
    return send_review_email(name, email, review)