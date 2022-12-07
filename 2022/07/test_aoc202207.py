"""Tests for AoC 7, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202207
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202207.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202207.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == {
        "a": {"e": {"i": 584}, "f": 29116, "g": 2557, "h.lst": 62596},
        "b.txt": 14848514,
        "c.dat": 8504156,
        "d": {"j": 4060174, "d.log": 8033020, "d.ext": 5626152, "k": 7214296},
    }


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202207.part1(example1) == 95437


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202207.part2(example1) == 24933642


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202207.part2(example2) == ...
