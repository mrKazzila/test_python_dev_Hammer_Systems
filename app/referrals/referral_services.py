from random import choice
from string import ascii_lowercase, ascii_uppercase, digits


def generate_referral_code(length: int = 6) -> str:
    """Generate a random referral code of the specified length."""
    chars = ascii_uppercase + ascii_lowercase + digits

    return ''.join(choice(chars) for _ in range(length))


def create_referral_code_for_user(user_obj, referral_code_model):
    """Create referral code for user."""
    referral, _ = referral_code_model.objects.get_or_create(owner=user_obj)
    code = str(referral.referral_code)

    return code
