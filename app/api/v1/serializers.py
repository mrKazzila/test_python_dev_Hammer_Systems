import logging

from rest_framework import serializers

from referrals.models import ReferralCode
from users.models import User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user.

    Fields:
        username: The user's username.
    """

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'used_referral_code')


class ReferralCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for the referral code.

    Fields:
        owner: The owner of the referral code.
        referral_code: The referral code.
    """

    class Meta:
        model = ReferralCode
        fields = ('phone',)

    phone = serializers.SerializerMethodField(source='get_owner_phone')

    def get_phone(self, obj):
        return obj.get_owner_phone


class UsersSerializer(serializers.ModelSerializer):
    """
    Serializer for the users.

    Fields:
        first_name: The user's first name.
        last_name: The user's last name.
        username: The user's username.
        phone_number: The user's phone number.
        referral_code: The user's referral code.
        referral_users_list: A list of the user's referral codes.
    """

    referral_users_list = ReferralCodeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'phone_number',
            'referral_code',
            'used_referral_code',
            'referral_users_list',
        )

    def update(self, instance, validated_data):
        # Overwrite the default update method to support writable nested fields.

        is_code_already_exist = instance.used_referral_code
        if is_code_already_exist != '':
            return instance

        referral_code = validated_data.get('referral_code')  # Referral code of instance user.
        used_referral_code = validated_data.get('used_referral_code')  # Referral code for add user instance.

        if referral_code == used_referral_code:
            return instance

        if used_referral_code:
            instance.used_referral_code = used_referral_code
            instance.save()
            logger.debug(f'Save referral code {used_referral_code=} for user {instance=}')

        # Update the referral_users_list field of the referral code's owner.
        # Owner of referral code.
        referrer_ref_code_obj = ReferralCode.objects.filter(referral_code=used_referral_code).first()

        # User used referral code.
        referral_ref_code_obj = ReferralCode.objects.filter(referral_code=referral_code).first()

        logger.debug(f'Update the referral_users_list field of the referral codes owner {referrer_ref_code_obj=}')

        if referrer_ref_code_obj:
            referrer_user = referrer_ref_code_obj.owner
            referrer_user.referral_users_list.add(referral_ref_code_obj)
            referrer_user.save()

        return super().update(instance, validated_data)


class TokenSerializer(serializers.Serializer):
    """Serializer for the token."""

    code = serializers.CharField(required=True)
