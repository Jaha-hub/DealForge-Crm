import pytest

from src.backend.domain.user.value_objects.username.errors import InvalidUsernameLengthError, \
    InvalidUsernameFormatError, UsernameError, UnsupportedUsernameTypeError
from src.backend.domain.user.value_objects.username.value_object import Username


@pytest.mark.parametrize(
    'value, expected',
    [
        ("alex_dev", "alex_dev"),
        ("user2026", "user2026"),
        ("john_doe", "john_doe"),
        ("admin123", "admin123"),
        ("pro_tester", "pro_tester"),
        ("vector", "vector"),
        ("stark_ind", "stark_ind"),
        ("devops_lead", "devops_lead")
    ]
)
def test_valid_username(value, expected):
    assert Username(value).value == expected


@pytest.mark.parametrize(
    'value',
    [
    "a"
    "ab"
    "this_is_a_very_long_username_designed_specifically_to_exceed_the_standard_two_hundred_and_fifty_five_character_limit_of_a_database_field_it_repeats_meaningless_words_over_and_over_again_just_to_fill_up_the_space_and_reach_the_required_length_for_testing_256"
    ]
)
def test_length_invalid_username(value):
    with pytest.raises(InvalidUsernameLengthError):
        Username(value)

@pytest.mark.parametrize(
    'value',
    [
        "user name",
        " user",
        "user!",
        "admin#build",
        "ivan@work",
        ".double..dot",
        "-start-with-dash",
        "bad/format",
        "имя_пользователя"
    ]
)
def test_format_invalid_username(value):
    with pytest.raises(InvalidUsernameFormatError):
        Username(value)

@pytest.mark.parametrize(
    'value',
    [
        "1user",
        "_admin",
        "user.name",
        "test-user",
        "john doe",
        "ivan@work",
        "имя_пользователя",
        "user!",
        "",
        " user",
        "user ",
        "-test",
        ".test",
        "user#1",
        " "
    ]
)
def test_invalid_username(value):
    with pytest.raises(UsernameError):
        Username(value)

@pytest.mark.parametrize(
    "value",
    [
        1,
        [1, 2, 3],
        True,
        1.6
    ]
)
def test_unsupported_type_username(value):
    with pytest.raises(UnsupportedUsernameTypeError):
        Username(value)