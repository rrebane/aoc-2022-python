"""Tests for AoC 22, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202222
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202222.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202222.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == (
        [
            [" ", " ", " ", " ", " ", " ", " ", " ", ".", ".", ".", "#"],
            [" ", " ", " ", " ", " ", " ", " ", " ", ".", "#", ".", "."],
            [" ", " ", " ", " ", " ", " ", " ", " ", "#", ".", ".", "."],
            [" ", " ", " ", " ", " ", " ", " ", " ", ".", ".", ".", "."],
            [".", ".", ".", "#", ".", ".", ".", ".", ".", ".", ".", "#"],
            [".", ".", ".", ".", ".", ".", ".", ".", "#", ".", ".", "."],
            [".", ".", "#", ".", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
            [
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                ".",
                ".",
                ".",
                "#",
                ".",
                ".",
                ".",
                ".",
            ],
            [
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                ".",
                ".",
                ".",
                ".",
                ".",
                "#",
                ".",
                ".",
            ],
            [
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                ".",
                "#",
                ".",
                ".",
                ".",
                ".",
                ".",
                ".",
            ],
            [
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                " ",
                ".",
                ".",
                ".",
                ".",
                ".",
                ".",
                "#",
                ".",
            ],
        ],
        [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5],
    )


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202222.part1(example1) == 6032


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202222.part2(example1) == 5031


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202222.part2(example2) == ...
