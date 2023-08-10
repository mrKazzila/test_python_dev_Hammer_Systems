from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from referrals.models import ReferralCode
from .user_services import generate_activation_code


class User(AbstractUser):
    """User model."""

    username = models.CharField(
        verbose_name='Username',
        max_length=25,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=30,
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name='Phone number',
        max_length=11,
        blank=True,
        unique=True,
    )

    referral_code = models.CharField(
        verbose_name='Referral code',
        max_length=6,
        blank=True,
    )
    used_referral_code = models.CharField(
        verbose_name='Used referral code',
        max_length=6,
        blank=True,
    )
    referral_code_list = models.ManyToManyField(
        ReferralCode,
        verbose_name='List of referral users',
        through='AddReferralCode'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username', )

    def __str__(self):
        return self.username


class ActivationCode(models.Model):
    """Model of activation code."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    code = models.CharField(
        max_length=4,
        default=generate_activation_code,
    )

    class Meta:
        verbose_name = 'activation code'
        verbose_name_plural = 'activation codes'

    def __str__(self):
        return self.code


class AddReferralCode(models.Model):
    """Model for adding an invitation code."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Adding a referral code'
        verbose_name_plural = 'Adding referral codes'

    def __str__(self):
        return f'{self.user} - {self.referral_code}'
