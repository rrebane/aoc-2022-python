"""Tests for AoC 10, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202210
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent
PART2_EXAMPLE1_RESULT = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202210.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202210.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        ("addx", 15),
        ("addx", -11),
        ("addx", 6),
        ("addx", -3),
        ("addx", 5),
        ("addx", -1),
        ("addx", -8),
        ("addx", 13),
        ("addx", 4),
        ("noop",),
        ("addx", -1),
        ("addx", 5),
        ("addx", -1),
        ("addx", 5),
        ("addx", -1),
        ("addx", 5),
        ("addx", -1),
        ("addx", 5),
        ("addx", -1),
        ("addx", -35),
        ("addx", 1),
        ("addx", 24),
        ("addx", -19),
        ("addx", 1),
        ("addx", 16),
        ("addx", -11),
        ("noop",),
        ("noop",),
        ("addx", 21),
        ("addx", -15),
        ("noop",),
        ("noop",),
        ("addx", -3),
        ("addx", 9),
        ("addx", 1),
        ("addx", -3),
        ("addx", 8),
        ("addx", 1),
        ("addx", 5),
        ("noop",),
        ("noop",),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", -36),
        ("noop",),
        ("addx", 1),
        ("addx", 7),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", 2),
        ("addx", 6),
        ("noop",),
        ("noop",),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", 1),
        ("noop",),
        ("noop",),
        ("addx", 7),
        ("addx", 1),
        ("noop",),
        ("addx", -13),
        ("addx", 13),
        ("addx", 7),
        ("noop",),
        ("addx", 1),
        ("addx", -33),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", 2),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", 8),
        ("noop",),
        ("addx", -1),
        ("addx", 2),
        ("addx", 1),
        ("noop",),
        ("addx", 17),
        ("addx", -9),
        ("addx", 1),
        ("addx", 1),
        ("addx", -3),
        ("addx", 11),
        ("noop",),
        ("noop",),
        ("addx", 1),
        ("noop",),
        ("addx", 1),
        ("noop",),
        ("noop",),
        ("addx", -13),
        ("addx", -19),
        ("addx", 1),
        ("addx", 3),
        ("addx", 26),
        ("addx", -30),
        ("addx", 12),
        ("addx", -1),
        ("addx", 3),
        ("addx", 1),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", -9),
        ("addx", 18),
        ("addx", 1),
        ("addx", 2),
        ("noop",),
        ("noop",),
        ("addx", 9),
        ("noop",),
        ("noop",),
        ("noop",),
        ("addx", -1),
        ("addx", 2),
        ("addx", -37),
        ("addx", 1),
        ("addx", 3),
        ("noop",),
        ("addx", 15),
        ("addx", -21),
        ("addx", 22),
        ("addx", -6),
        ("addx", 1),
        ("noop",),
        ("addx", 2),
        ("addx", 1),
        ("noop",),
        ("addx", -10),
        ("noop",),
        ("noop",),
        ("addx", 20),
        ("addx", 1),
        ("addx", 2),
        ("addx", 2),
        ("addx", -6),
        ("addx", -11),
        ("noop",),
        ("noop",),
        ("noop",),
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202210.part1(example1) == 13140


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202210.part2(example1) == PART2_EXAMPLE1_RESULT


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202210.part2(example2) == ...
