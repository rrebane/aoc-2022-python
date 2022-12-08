"""Tests for AoC 8, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202208
import numpy as np
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202208.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202208.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert np.array_equal(
        example1,
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ],
    )


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202208.part1(example1) == 21


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202208.part2(example1) == 8


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202208.part2(example2) == ...
