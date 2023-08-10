import random
from string import digits


def generate_activation_code():
    """Generate a random activation code."""
    return ''.join(random.choice(digits) for _ in range(4))
