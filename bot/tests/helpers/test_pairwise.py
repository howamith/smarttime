from typing import List
import pytest

from bot.helpers.pairwise import pairwise


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        (
            [True, False, True, False],
            [(True, False), (False, True), (True, False)],
        ),
        ([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)]),
        (
            [0.1, 0.2, 0.3, 0.4, 0.5],
            [(0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5)],
        ),
        (
            ["abc", "def", "ghi", "jkl"],
            [("abc", "def"), ("def", "ghi"), ("ghi", "jkl")],
        ),
    ],
)
def test_pairwise_pairs_primitive(input: list, expected: List[tuple]):
    """Test that pairwise can pair primitve types."""
    assert list(pairwise(input)) == expected
