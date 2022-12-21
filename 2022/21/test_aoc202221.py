"""Tests for AoC 21, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202221
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202221.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202221.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        ("root", ("+", "pppw", "sjmn")),
        ("dbpl", 5),
        ("cczh", ("+", "sllz", "lgvd")),
        ("zczc", 2),
        ("ptdq", ("-", "humn", "dvpt")),
        ("dvpt", 3),
        ("lfqf", 4),
        ("humn", 5),
        ("ljgn", 2),
        ("sjmn", ("*", "drzm", "dbpl")),
        ("sllz", 4),
        ("pppw", ("/", "cczh", "lfqf")),
        ("lgvd", ("*", "ljgn", "ptdq")),
        ("drzm", ("-", "hmdt", "zczc")),
        ("hmdt", 32),
    ]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202221.part1(example1) == 152


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202221.part2(example1) == 301


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202221.part2(example2) == ...
