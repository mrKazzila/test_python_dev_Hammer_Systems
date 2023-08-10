import logging
import time

from config.celery import app
from .models import ActivationCode, User

logger = logging.getLogger(__name__)


@app.task
def send_activation_code(username):
    """Task for send activation code."""
    user = User.objects.get(username=username)
    logger.info(f'Send activation code for {username}')

    code = ActivationCode.objects.create(user=user)
    logger.info(f'ActivationCode for {user.username} is {code.code}')

    # Some service for sms sending
    time.sleep(2)

    return code.code
