from string import ascii_lowercase, ascii_uppercase, digits

import pytest

from ..referral_services import generate_referral_code


def test_generate_referral_code_with_default_length():
    """Test that the generate_referral_code() function generates a 6-character referral code."""
    referral_code = generate_referral_code()

    assert len(referral_code) == 6


def test_generate_referral_code_with_custom_length():
    """Test that the generate_referral_code() function generates a referral code of the specified length."""
    referral_code = generate_referral_code(length=10)

    assert len(referral_code) == 10


@pytest.mark.parametrize('bad_length_value, error_type', [
    ('', TypeError),
    ('abc', TypeError),
])
def test_generate_referral_code_with_invalid_length(bad_length_value, error_type):
    """Test that the generate_referral_code() function raises an exception when the specified length is invalid."""
    with pytest.raises(error_type):
        generate_referral_code(length=bad_length_value)


def test_generate_referral_code_with_valid_characters():
    """The generate_referral_code() function should generate a random referral code with valid characters."""
    code = generate_referral_code()
    chars = ascii_uppercase + ascii_lowercase + digits

    assert all(c in chars for c in code)


def test_generate_referral_code_uniqueness():
    """Test that the generated referral codes are unique."""
    codes = [generate_referral_code(length=6) for _ in range(50)]

    assert len(set(codes)) == 50
