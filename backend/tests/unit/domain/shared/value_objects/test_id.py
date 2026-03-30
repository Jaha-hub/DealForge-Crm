import pytest

from src.backend.domain.shared.value_objects.id.errors import NegativeIntIdError, UnsupportedTypeIdError
from src.backend.domain.shared.value_objects.id.value_object import Id



@pytest.mark.parametrize(
    "value, expected",
    [
        (1,1),
        (100,100),
        (1000,1000)
     ]
)
def test_valid_id(value, expected):
    assert Id(value).value == expected

@pytest.mark.parametrize(
    "value",
    [
        1.6,
        "1",
        {1},
        {"id":1}
    ]
)
def test_unsupported_type_id(value):
    with pytest.raises(UnsupportedTypeIdError):
        Id(value)


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -251
    ]
)
def test_negative_value(value):
    with pytest.raises(NegativeIntIdError):
        Id(value)