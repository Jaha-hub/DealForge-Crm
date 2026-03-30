import pytest

from src.backend.domain.shared.value_objects.name.errors import InvalidNameError, NameTypeError, NameLengthError
from src.backend.domain.shared.value_objects.name.value_object import Name


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Анна", "Анна"),
        ("John", "John"),
        ("Ян", "Ян"),
        ("Александр", "Александр"),
        ("Elizabeth", "Elizabeth"),
        ("п" * 255, "п" * 255),
        ("Оливия", "Оливия"),
        ("Maximilian", "Maximilian"),
        ("Ия", "Ия"),
        ("п" * 100, "п" * 100)
    ]
)
def test_valid_name(value,expected):
    assert Name(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1,
        [1, 2, 3],
        True,
        None,
        1.6,
        {"name": "Ivan"}
    ]
)
def test_type_invalid_name(value):
    with pytest.raises(NameTypeError):
        Name(value)


@pytest.mark.parametrize(
    "value",
    [
        "Иван1",
        "123",
        "007Агент",
        "John_Doe",
        "Alex!",
        "Ivan#",
        "M@x",
        "Petr.Ivanov",
        "Anna-Maria",
        "Иван Иванов"
    ]
)
def test_invalid_name_format(value):
    with pytest.raises(InvalidNameError):
        Name(value)



@pytest.mark.parametrize(
    "value",
    [
        "",
        "А",
        "a" * 256,
        " "
    ]
)
def test_invalid_name_length(value):
    with pytest.raises(NameLengthError):
        Name(value)