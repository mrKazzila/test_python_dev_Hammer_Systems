from string import digits

from ..user_services import generate_activation_code


def test_generate_activation_code_length():
    """Test that the activation code is 4 digits long."""
    code = generate_activation_code()
    assert len(code) == 4


def test_generate_activation_code_contains_digits():
    """Test that the activation code contains only digits."""
    code = generate_activation_code()
    for digit in code:
        assert digit in digits


def test_generate_activation_code_is_random():
    """Test that the activation code is random."""
    codes = [generate_activation_code() for _ in range(20)]
    assert len(set(codes)) == 20
