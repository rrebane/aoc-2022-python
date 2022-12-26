"""AoC 20, 2022."""

import pathlib
import sys

import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    return [int(line) for line in puzzle_input.split("\n")]


def mix(enc, perm):
    for val_idx, val in enumerate(enc):
        idx = np.argsort(perm)[val_idx]

        steps = val % (len(enc) - 1)
        new_idx = (idx + steps) % len(enc)

        tmp = perm[idx]

        if new_idx > idx:
            perm[idx:new_idx] = perm[idx+1:new_idx+1]
            perm[new_idx] = tmp
        elif new_idx + 1 < idx:
            perm[new_idx+2:idx+1] = perm[new_idx+1:idx]
            perm[new_idx+1] = tmp

    return perm.copy()


def part1(data):
    """Solve part 1."""
    enc = np.array(data, dtype=np.int32)
    perm = np.array(range(len(enc)), dtype=np.uint16)

    perm = mix(enc, perm)
    idx = np.argmax(perm == np.argmax(enc == 0))

    numbers = [
        enc[perm[(idx + 1000) % len(enc)]],
        enc[perm[(idx + 2000) % len(enc)]],
        enc[perm[(idx + 3000) % len(enc)]],
    ]

    return sum(numbers)


def part2(data):
    """Solve part 2."""
    enc = np.array(data, dtype=np.int64)
    perm = np.array(range(len(enc)), dtype=np.uint16)

    enc *= 811589153

    for _ in range(10):
        perm = mix(enc, perm)

    idx = np.argmax(perm == np.argmax(enc == 0))

    numbers = [
        enc[perm[(idx + 1000) % len(enc)]],
        enc[perm[(idx + 2000) % len(enc)]],
        enc[perm[(idx + 3000) % len(enc)]],
    ]

    return sum(numbers)


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
