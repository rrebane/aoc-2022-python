"""Tests for AoC 14, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202214
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202214.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202214.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        [(498, 4), (498, 6), (496, 6)],
        [(503, 4), (502, 4), (502, 9), (494, 9)],
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202214.part1(example1) == 24


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202214.part2(example1) == 93


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202214.part2(example2) == ...
