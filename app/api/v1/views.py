import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView

from referrals.models import ReferralCode
from referrals.referral_services import create_referral_code_for_user
from users.models import ActivationCode, User
from users.tasks import send_activation_code
from users.user_services import (
    delete_referral_code_for_authenticated_user,
    generate_token_for_user,
    make_dict_obj_from_request_data,
)
from .serializers import TokenSerializer, UserSerializer, UsersSerializer

logger = logging.getLogger(__name__)


class CreateUserAndSendConfirmCodeView(APIView):
    """Creates a user and sends a confirmation code to the user's phone number."""

    permission_classes = [AllowAny]
    allowed_methods = ['POST', 'OPTIONS']

    def post(self, request):
        """Create a user and sends a confirmation code to the user's phone number.

        Args:
            request: The HTTP request.

        Returns:
            The HTTP response.
        """
        request_data = make_dict_obj_from_request_data(request_data=request.data)
        serializer = UserSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get('username')
        phone_number = serializer.data.get('phone_number')
        user, created = User.objects.get_or_create(username=username, phone_number=phone_number)

        if not created:
            return Response(status=HTTP_400_BAD_REQUEST)

        # Fake send activation code.
        task = send_activation_code.delay(username)
        # Just for example. Cos '.get()' make execution task by sync.
        code = task.get(timeout=3)

        logger.info(f'Created user {user.username} with confirmation code {code}')
        return Response({'code': str(code)}, status=HTTP_200_OK)


class GenerateTokenAndReferralCodeView(APIView):
    """Generate a token and referral code for the user and returns them."""

    permission_classes = [AllowAny]
    allowed_methods = ['POST', 'DELETE', 'OPTIONS']

    def post(self, request):
        """
        Check the activation code and returns the user token and referral code.

        Args:
            request: The HTTP request.

        Returns:
            The HTTP response.
        """
        request_data = make_dict_obj_from_request_data(request_data=request.data)
        serializer = TokenSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        code_value = serializer.data.get('code')
        activation_code = get_object_or_404(ActivationCode, code=code_value)

        if not activation_code:
            logger.warning('Activation code not found')
            return Response('Activation code not found', status=HTTP_400_BAD_REQUEST)

        user = activation_code.user
        activation_code.delete()

        logger.info(f'Generating referral code and token for user {user.username}')
        referral_code = create_referral_code_for_user(user_obj=user, referral_code_model=ReferralCode)
        token = generate_token_for_user(user_obj=user, user_model=User)

        user.referral_code = referral_code
        user.save()

        response_data = {'token': str(token), 'referral code': referral_code}
        return Response(response_data, status=HTTP_200_OK)

    def delete(self, request):
        """
        Delete the referral code for the authenticated user.

        Args:
            request: The HTTP request.

        Returns:
            The HTTP response.
        """
        user = request.user

        if user:
            referral = ReferralCode.objects.filter(owner=user).first()
            return delete_referral_code_for_authenticated_user(referral_obj=referral)

        logger.warning('User not authenticated')
        return Response('User is not authenticated', status=HTTP_401_UNAUTHORIZED)


class CurrentUserViewSet(viewsets.ModelViewSet):
    """Viewset provides an API for users to get and edit their own data."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
