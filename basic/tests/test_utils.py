import pytest

from basic import utils


@pytest.mark.parametrize('my_list, expected', [
    ([1, 2, 3], 6),
    (['hello', 10, 'world!', 12], 22),
    ([1.1, 20, 10, 'message'], 30),
])
def test_sum_of_list_numbers(my_list, expected):
    result = utils.sum_of_list_numbers(my_list)

    assert result
    assert isinstance(result, int)
    assert result == expected
