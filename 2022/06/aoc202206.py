"""AoC 6, 2022."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    return puzzle_input


def is_distinct(sequence):
    return len(set(sequence)) == len(sequence)


def part1(data):
    """Solve part 1."""
    for i in range(4, len(data)):
        if is_distinct(data[i - 4 : i]):
            return i


def part2(data):
    """Solve part 2."""
    for i in range(14, len(data)):
        if is_distinct(data[i - 14 : i]):
            return i


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
