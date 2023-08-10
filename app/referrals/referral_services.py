from random import choice
from string import ascii_lowercase, ascii_uppercase, digits


def generate_referral_code(length: int = 6) -> str:
    """Generate a random referral code of the specified length."""
    chars = ascii_uppercase + ascii_lowercase + digits
    return ''.join(choice(chars) for _ in range(length))
