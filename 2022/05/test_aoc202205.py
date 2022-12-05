"""Tests for AoC 5, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202205
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text()
    return aoc202205.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text()
    return aoc202205.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == aoc202205.Data(
        stacks=[["Z", "N"], ["M", "C", "D"], ["P"]],
        instructions=[(1, 1, 0), (3, 0, 2), (2, 1, 0), (1, 0, 1)],
    )


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202205.part1(example1) == "CMZ"


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202205.part2(example1) == "MCD"


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202205.part2(example2) == ...
