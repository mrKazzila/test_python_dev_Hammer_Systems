import pytest
from django.db import IntegrityError
from django.test import TestCase

from referrals.models import ReferralCode
from users.models import ActivationCode, AddReferralCode, User


class UserTest(TestCase):
    """Tests for User model."""

    @pytest.mark.django_db
    def test_user_can_be_created_with_phone_number(self):
        """
        Tests that a `User` instance can be created with a phone number.

        The phone number should be stored in the `phone_number` field.
        The `referral_code` field should be empty.
        """
        phone_number = '+1234567890'
        user = User.objects.create(phone_number=phone_number)

        assert user.phone_number == phone_number
        assert user.referral_code == ''

    @pytest.mark.django_db
    def test_user_cannot_be_created_without_phone_number(self):
        """
        Tests that a `User` instance cannot be created without a phone number.

        If the `phone_number` field is not set, an `IntegrityError` exception should be raised.
        """
        with pytest.raises(IntegrityError):
            User.objects.create(phone_number=None, referral_code='123456')

    @pytest.mark.django_db
    def test_user_cannot_be_created_with_duplicate_phone_number(self):
        """
        Tests that a `User` instance cannot be created with a duplicate phone number.

        If the `phone_number` field already exists in the database, an `IntegrityError` exception should be raised.
        """
        phone_number = '+1234567890'
        User.objects.create(phone_number=phone_number)

        with pytest.raises(IntegrityError):
            User.objects.create(phone_number=phone_number)

    @pytest.mark.django_db
    def test_user_can_be_created_with_used_referral_code(self):
        """
        Tests that a `User` instance can be created with a used referral code.

        The `used_referral_code` field should be set to the referral code.
        """
        used_referral_code = '123456'
        user = User.objects.create(used_referral_code=used_referral_code)

        assert user.used_referral_code == used_referral_code


class ActivationCodeTest(TestCase):
    """Tests for ActivationCode model."""

    @pytest.mark.django_db
    def test_activation_code_can_be_created(self):
        """
        Tests that an `ActivationCode` instance can be created.

        The `user` field should be set to the user who created the activation code.
        The `code` field should be a randomly generated 4-digit code.
        """
        phone_number = '+1234567890'
        user = User.objects.create(phone_number=phone_number)
        activation_code = ActivationCode.objects.create(user=user)

        assert activation_code.user == user
        assert activation_code.code == str(activation_code)
        assert len(activation_code.code) == 4

    @pytest.mark.django_db
    def test_activation_code_cannot_be_created_without_user(self):
        """
        Tests that an `ActivationCode` instance cannot be created without a user.

        If the `user` field is not set, an `IntegrityError` exception should be raised.
        """
        with pytest.raises(IntegrityError):
            ActivationCode.objects.create()


class AddReferralCodeTest(TestCase):
    """Tests for AddReferralCode model."""

    @pytest.mark.django_db
    def test_add_referral_code_can_be_created(self):
        """
        Tests that an `AddReferralCode` instance can be created.

        The `user` field should be set to the user who created the add referral code.
        The `referral_code` field should be set to the referral code.
        The `referral_code` field should be owned by the `user` field.
        """
        phone_number_1, phone_number_2 = '+1234567890', '+1234567891'
        user_1 = User.objects.create(phone_number=phone_number_1, username='Jhon')
        user_2 = User.objects.create(phone_number=phone_number_2, username='Bob')

        create_referral_code = ReferralCode.objects.create(owner=user_1)
        add_referral_code_by_user_1_for_user_2 = AddReferralCode.objects.create(
            user=user_2,
            referral_code=create_referral_code,
        )

        assert add_referral_code_by_user_1_for_user_2.user == user_2
        assert add_referral_code_by_user_1_for_user_2.referral_code == create_referral_code
        assert add_referral_code_by_user_1_for_user_2.referral_code.owner == user_1

    @pytest.mark.django_db
    def test_add_referral_code_cannot_be_created_without_user(self):
        """
        Tests that an `AddReferralCode` instance cannot be created without a user.

        If the `user` field is not set, a `ValueError` exception should be raised.

        This test ensures that the `AddReferralCode` model cannot be used to create referral codes for
        users who do not exist.
        """
        with pytest.raises(ValueError):
            AddReferralCode.objects.create(referral_code='123456')

    @pytest.mark.django_db
    def test_add_referral_code_cannot_be_created_without_referral_code(self):
        """
        Tests that an `AddReferralCode` instance cannot be created without a referral code.

        If the `referral_code` field is not set, an `IntegrityError` exception should be raised.

        This test ensures that the `AddReferralCode` model cannot be used to create referral codes that do not exist.
        """
        user = User.objects.create(phone_number='+1234567890', username='Jhon')

        with pytest.raises(IntegrityError):
            AddReferralCode.objects.create(user=user)
