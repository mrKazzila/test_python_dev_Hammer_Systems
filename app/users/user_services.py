import json
import logging
import random
from string import digits

from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

logger = logging.getLogger(__name__)


def generate_activation_code():
    """Generate a random activation code."""
    return ''.join(random.choice(digits) for _ in range(4))


def generate_token_for_user(user_obj, user_model):
    """Generate token for user."""
    user = user_model.objects.get(username=user_obj)
    token = default_token_generator.make_token(user)

    return token


def delete_referral_code_for_authenticated_user(referral_obj):
    """Delete the referral code for the authenticated user."""
    if referral_obj:
        referral_obj.delete()
        logger.info('Referral code deleted')
        return Response('Referral code successfully deleted', status=HTTP_204_NO_CONTENT)

    logger.warning('Referral code not found')
    return Response('Referral code not found', status=HTTP_404_NOT_FOUND)


def make_dict_obj_from_request_data(request_data):
    """Create a dict object from the request data."""
    logger.info(f'request_data={type(request_data)}')

    if type(request_data) == dict:
        return request_data

    query_dict_to_dict = request_data.dict()
    _content = query_dict_to_dict.get('_content')

    return json.loads(_content)
