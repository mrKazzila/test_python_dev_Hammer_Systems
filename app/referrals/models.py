from django.conf import settings
from django.db import models

from .referral_services import generate_referral_code


class ReferralCode(models.Model):
    """Referral Code Model."""

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='Referral code owner',
        on_delete=models.CASCADE,
    )
    referral_code = models.CharField(
        verbose_name='Referral code',
        max_length=6,
        default=generate_referral_code,
    )

    class Meta:
        verbose_name = 'Referral code'
        verbose_name_plural = 'Referral codes'

    def __str__(self):
        return f'User {self.owner} is owner referral code {self.referral_code}'

    @property
    def get_owner_phone(self):
        return self.owner.phone_number
