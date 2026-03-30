import pytest

from src.backend.domain.shared.value_objects.email.errors import InvalidEmailError
from src.backend.domain.shared.value_objects.email.value_object import Email


@pytest.mark.parametrize(
    "value, expected",
    [
        ("user1@example.com", "user1@example.com"),
        ("test_user@example.com", "test_user@example.com"),
        ("admin@example.com", "admin@example.com"),
        ("support@example.org", "support@example.org"),
        ("dev_test@example.net", "dev_test@example.net"),
        ("info@example.com", "info@example.com"),
        ("marketing@example.com", "marketing@example.com"),
        ("sales@example.org", "sales@example.org"),
        ("billing@example.net", "billing@example.net"),
        ("guest@example.com", "guest@example.com"),
    ]
)
def test_valid_email(value, expected):
    assert Email(value).value== expected

@pytest.mark.parametrize(
    "value",[
    "plainaddress"
    "#@%^%#$@#$@#.com"
    "@example.com"
    "Joe Smith <email@example.com>"
    "email.example.com"
    "email@example@example.com"
    ".email@example.com"
    "email.@example.com"
    "email..email@example.com"
    "email@-example.com"
]
)
def test_invalid_email(value):
    with pytest.raises(InvalidEmailError):
        Email(value)