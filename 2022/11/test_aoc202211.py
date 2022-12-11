"""Tests for AoC 11, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202211
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202211.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202211.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        ([79, 98], ("*", 19), (23, 2, 3)),
        ([54, 65, 75, 74], ("+", 6), (19, 2, 0)),
        ([79, 60, 97], ("*", None), (13, 1, 3)),
        ([74], ("+", 3), (17, 0, 1)),
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202211.part1(example1) == 10605


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202211.part2(example1) == 2713310158


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202211.part2(example2) == ...
