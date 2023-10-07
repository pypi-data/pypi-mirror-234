import pytest

from json_logic import jsonLogic


@pytest.mark.unsupported_operators(["filter", "all", "none", "some", "substr"])
@pytest.mark.unsupported_logic(
    [
        {"var": []},
    ]
)
def test_shared_test(shared_test):
    """
    Test the shared JSON tests one-by-one.

    ``logic`` combined with ``data`` must yield ``expected`` result.
    """
    logic, data, expected = shared_test

    result = jsonLogic(logic, data)

    assert result == expected
