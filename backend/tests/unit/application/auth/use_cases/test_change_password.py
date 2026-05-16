import pytest

from src.backend.application.auth.errors import WeakPasswordError
from src.backend.domain.user.value_objects.password.value_object import Password


@pytest.fixture()
def valid_password() -> Password:
    return Password("StrongPass1!")


@pytest.fixture()
def another_valid_password() -> Password:
    return Password("AnotherPass2@")


def make_password(value: str) -> Password:
    return Password(value=value)


def test_successful_password_creation(valid_password: Password):
    assert valid_password.value == "StrongPass1!"


def test_password_raises_too_short():
    with pytest.raises(WeakPasswordError):
        make_password("Sh0rt!")


def test_password_raises_no_uppercase():
    with pytest.raises(WeakPasswordError):
        make_password("nouppercase1!")


def test_password_raises_no_lowercase():
    with pytest.raises(WeakPasswordError):
        make_password("NOLOWERCASE1!")


def test_password_raises_no_digit():
    with pytest.raises(WeakPasswordError):
        make_password("NoDigitPass!")


def test_password_raises_no_special_char():
    with pytest.raises(WeakPasswordError):
        make_password("NoSpecial1234")


def test_is_same_as_returns_true(valid_password: Password):
    same = make_password(valid_password.value)
    assert valid_password.is_same_as(same) is True


def test_is_same_as_returns_false(valid_password: Password, another_valid_password: Password):
    assert valid_password.is_same_as(another_valid_password) is False