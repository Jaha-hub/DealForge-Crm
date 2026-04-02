import pytest

from src.backend.domain.shared.value_objects.email.errors import InvalidEmailError
from src.backend.domain.shared.value_objects.email.value_object import Email

@pytest.fixture
def test_email():
    return Email("testuser@gmail.com")

@pytest.mark.parametrize(
    "value, expected",
    [
        ("alex.smith@gmail.com", "alex.smith@gmail.com"),
        ("user123@yahoo.com", "user123@yahoo.com"),
        ("john_doe@outlook.com", "john_doe@outlook.com"),
        ("test.email@protonmail.com", "test.email@protonmail.com"),
        ("info.company@mail.com", "info.company@mail.com"),
        ("anna.karimova@gmail.com", "anna.karimova@gmail.com"),
        ("dev.team@company.org", "dev.team@company.org"),
        ("student2026@university.edu", "student2026@university.edu"),
        ("contact-us@service.net", "contact-us@service.net"),
        ("my.emailalias@gmail.com", "my.emailalias@gmail.com"),
    ]
)
def test_email_validation(value, expected):
    # Здесь должна быть логика вашего теста, например:
    # assert some_processing_function(value) == expected
    assert Email(value).value == expected

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