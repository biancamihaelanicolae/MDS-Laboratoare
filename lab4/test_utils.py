import pytest
from utils import clamp, merge_sorted, parse_pair, unique_sorted


def test_clamp_inside():
    assert clamp(5, 0, 10) == 5


def test_clamp_below():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above():
    assert clamp(15, 0, 10) == 10


def test_clamp_low_boundary():
    assert clamp(0, 0, 10) == 0


def test_clamp_high_boundary():
    assert clamp(10, 0, 10) == 10


def test_clamp_lo_eq_hi():
    assert clamp(7, 5, 5) == 5
    assert clamp(3, 5, 5) == 5


def test_merge_sorted_normal():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]


def test_merge_sorted_first_empty():
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]


def test_merge_sorted_second_empty():
    assert merge_sorted([1, 2, 3], []) == [1, 2, 3]


def test_merge_sorted_both_empty():
    assert merge_sorted([], []) == []


def test_merge_sorted_duplicates():
    assert merge_sorted([1, 2, 2], [2, 3, 4]) == [1, 2, 2, 2, 3, 4]


def test_parse_pair_valid():
    assert parse_pair("3:5") == (3, 5)


def test_parse_pair_no_separator():
    with pytest.raises(ValueError):
        parse_pair("hello")


def test_parse_pair_extra_separator():
    with pytest.raises(ValueError):
        parse_pair("a:b:c")


def test_parse_pair_non_numeric():
    with pytest.raises(ValueError):
        parse_pair("a:5")


def test_parse_pair_empty():
    with pytest.raises(ValueError):
        parse_pair("")


def test_unique_sorted_normal():
    assert unique_sorted([3, 1, 2, 1, 2]) == [1, 2, 3]


def test_unique_sorted_bug_consecutive_duplicates():
    """unique_sorted has a bug: triple consecutive duplicates fail."""
    assert unique_sorted([1, 1, 1]) == [1]
