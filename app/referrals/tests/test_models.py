import pytest
from django.test import TestCase

from referrals.models import ReferralCode
from users.models import User


class ReferralCodeTest(TestCase):

    @pytest.mark.django_db
    def test_referral_code_creation(self):
        """Test that a ReferralCode can be created."""
        user = User.objects.create(phone_number='+1234567890', username='Jhon')
        referral_code = ReferralCode.objects.create(owner=user)

        assert referral_code.owner == user
        assert len(referral_code.referral_code) == 6

    @pytest.mark.django_db
    def test_referral_code_uniqueness(self):
        """Test that a ReferralCode with the same code cannot be created twice."""
        user = User.objects.create(phone_number='+1234567890', username='Jhon')
        first_code = ReferralCode.objects.create(owner=user)

        ReferralCode.objects.get(owner=user).delete()

        second_code = ReferralCode.objects.create(owner=user)

        assert first_code.referral_code != second_code.referral_code
        assert first_code.owner == second_code.owner

    @pytest.mark.django_db
    def test_referral_code_str(self):
        """Test that the ReferralCode.__str__() method returns the correct string."""
        user = User.objects.create(phone_number='+1234567890', username='Jhon')
        referral_code = ReferralCode.objects.create(owner=user, referral_code='ABC123')

        assert str(referral_code) == f'User {user} is owner referral code {referral_code.referral_code}'
