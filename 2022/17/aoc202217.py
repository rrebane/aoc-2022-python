"""AoC 17, 2022."""

import numpy as np
import pathlib
import sys


def parse_data(puzzle_input):
    return puzzle_input


def rock_shapes():
    return [
        np.array([[1, 1, 1, 1]], dtype=np.int8),
        np.array(
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
            dtype=np.int8,
        ),
        np.array(
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1],
            ],
            dtype=np.int8,
        ),
        np.array(
            [
                [1],
                [1],
                [1],
                [1],
            ],
            dtype=np.int8,
        ),
        np.array(
            [
                [1, 1],
                [1, 1],
            ],
            dtype=np.int8,
        ),
    ]


def height_to_y(cave, height):
    return cave.shape[0] - height


def y_to_height(cave, y):
    return cave.shape[0] - y


def can_move_to(cave, rock, loc):
    cave_h, cave_w = cave.shape
    rock_h, rock_w = rock.shape
    x, y = loc

    if x < 0 or y < 0 or x + rock_w > cave_w or y + rock_h > cave_h:
        return False

    if np.any((cave[y : y + rock_h, x : x + rock_w] + rock) > 1):
        return False

    return True


def move_rock(cave, rock, jet, rock_loc):
    rock_x, rock_y = rock_loc

    match jet:
        case ">":
            if can_move_to(cave, rock, (rock_x + 1, rock_y)):
                rock_x += 1
        case "<":
            if can_move_to(cave, rock, (rock_x - 1, rock_y)):
                rock_x -= 1

    stop = False

    if can_move_to(cave, rock, (rock_x, rock_y + 1)):
        rock_y += 1
    else:
        stop = True

    return (stop, (rock_x, rock_y))


def simulate_cave(data, simulate_n_rocks):
    rocks = rock_shapes()

    cave = np.zeros((simulate_n_rocks * 4, 7), dtype=np.int8)
    height_changes = [0]

    simulation_step = 0

    for rock_nr in range(simulate_n_rocks):
        rock = rocks[rock_nr % len(rocks)]
        tower_height = sum(height_changes)
        rock_x, rock_y = (2, height_to_y(cave, tower_height + 3 + rock.shape[0]))
        stop = False

        while not stop:
            jet = data[simulation_step % len(data)]
            stop, (rock_x, rock_y) = move_rock(cave, rock, jet, (rock_x, rock_y))

            simulation_step += 1

        cave[rock_y : rock_y + rock.shape[0], rock_x : rock_x + rock.shape[1]] += rock

        height_changes.append(
            max(tower_height, y_to_height(cave, rock_y)) - tower_height
        )

    return height_changes[1:]


def part1(data, simulate_n_rocks=2022):
    """Solve part 1."""
    height_changes = simulate_cave(data, simulate_n_rocks)
    return sum(height_changes)


def part2(data, simulate_n_rocks=1000000000000):
    """Solve part 2."""
    search_len = len(data)
    height_changes = simulate_cave(data, search_len * 4)

    pattern_idxs = []

    for i in range(len(height_changes) - search_len):
        if height_changes[i : i + search_len] == height_changes[-search_len:]:
            pattern_idxs.append(i)

            if len(pattern_idxs) > 1:
                break

    pattern_period = pattern_idxs[1] - pattern_idxs[0]
    pattern_height = sum(height_changes[pattern_idxs[0] : pattern_idxs[1]])

    pattern_mult = (simulate_n_rocks - pattern_idxs[0]) // pattern_period
    pattern_mod = (simulate_n_rocks - pattern_idxs[0]) % pattern_period

    th_start = sum(height_changes[: pattern_idxs[0]])
    th_end = sum(height_changes[pattern_idxs[0] : pattern_idxs[0] + pattern_mod])

    tower_height = th_start + pattern_mult * pattern_height + th_end

    return tower_height


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
