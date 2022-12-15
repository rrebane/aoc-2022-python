"""Tests for AoC 15, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202215
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202215.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202215.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        ((2, 18), (-2, 15)),
        ((9, 16), (10, 16)),
        ((13, 2), (15, 3)),
        ((12, 14), (10, 16)),
        ((10, 20), (10, 16)),
        ((14, 17), (10, 16)),
        ((8, 7), (2, 10)),
        ((2, 0), (2, 10)),
        ((0, 11), (2, 10)),
        ((20, 14), (25, 17)),
        ((17, 20), (21, 22)),
        ((16, 7), (15, 3)),
        ((14, 3), (15, 3)),
        ((20, 1), (15, 3)),
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202215.part1(example1, 10) == 26


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202215.part2(example1, ((0, 0), (20, 20))) == 56000011


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202215.part2(example2, None) == ...
