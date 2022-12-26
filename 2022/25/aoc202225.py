"""AoC 25, 2022."""

import pathlib
import sys


def parse_data(puzzle_input):
    return list(puzzle_input.split("\n"))


def snafu_to_decimal(snafu):
    decimal = 0

    for i, digit in enumerate(snafu[::-1]):
        match digit:
            case "=":
                decimal += -2 * pow(5, i)
            case "-":
                decimal += -1 * pow(5, i)
            case "0":
                decimal += 0
            case "1":
                decimal += 1 * pow(5, i)
            case "2":
                decimal += 2 * pow(5, i)
            case _:
                assert False

    return decimal


def decimal_to_snafu(decimal):
    digits = 1
    largest_decimal_for_digits = 2 * pow(5, digits - 1)
    digit_ranges = [0, 2]

    while decimal > largest_decimal_for_digits:
        digits += 1
        largest_decimal_for_digits += 2 * pow(5, digits - 1)
        digit_ranges.append(largest_decimal_for_digits)

    snafu = []

    while digits > 0:
        dbase = digit_ranges[digits - 1]
        drange = (digit_ranges[digits] - digit_ranges[digits - 1]) // 2

        if dbase + drange < decimal <= dbase + 2 * drange:
            decimal -= 2 * drange
            snafu.append("2")
        elif dbase < decimal <= dbase + drange:
            decimal -= drange
            snafu.append("1")
        elif -dbase <= decimal <= dbase:
            snafu.append("0")
        elif -dbase - drange <= decimal < -dbase:
            decimal += drange
            snafu.append("-")
        elif -dbase - 2 * drange <= decimal < -dbase - drange:
            decimal += 2 * drange
            snafu.append("=")

        digits -= 1

    return "".join(snafu)


def part1(data):
    """Solve part 1."""
    decimal_sum = sum(snafu_to_decimal(snafu) for snafu in data)
    return decimal_to_snafu(decimal_sum)


def part2(data):
    """Solve part 2."""


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
