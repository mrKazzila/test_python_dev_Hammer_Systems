from rest_framework import serializers

from referrals.models import ReferralCode
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user.

    Fields:
        username: The user's username.
    """

    class Meta:
        model = User
        fields = ('username', 'phone_number')


class ReferralCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for the referral code.

    Fields:
        owner: The owner of the referral code.
        referral_code: The referral code.
    """

    class Meta:
        model = ReferralCode
        fields = ('owner', 'referral_code')


class UsersSerializer(serializers.ModelSerializer):
    """
    Serializer for the users.

    Fields:
        first_name: The user's first name.
        last_name: The user's last name.
        username: The user's username.
        phone_number: The user's phone number.
        referral_code: The user's referral code.
        referral_code_list: A list of the user's referral codes.
    """

    referral_code_list = ReferralCodeSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'referral_code',
            'referral_code_list',
        )


class TokenSerializer(serializers.Serializer):
    """Serializer for the token."""

    code = serializers.CharField(required=True)
