"""Tests for AoC 16, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202216
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202216.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202216.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        ("AA", 0, ["DD", "II", "BB"]),
        ("BB", 13, ["CC", "AA"]),
        ("CC", 2, ["DD", "BB"]),
        ("DD", 20, ["CC", "AA", "EE"]),
        ("EE", 3, ["FF", "DD"]),
        ("FF", 0, ["EE", "GG"]),
        ("GG", 0, ["FF", "HH"]),
        ("HH", 22, ["GG"]),
        ("II", 0, ["AA", "JJ"]),
        ("JJ", 21, ["II"]),
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202216.part1(example1) == 1651


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202216.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202216.part2(example2) == ...
