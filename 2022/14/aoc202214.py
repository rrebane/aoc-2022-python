"""AoC 14, 2022."""

import math
import numpy as np
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_path(self, node, visited_children):
        coordinates, _ = visited_children
        return coordinates

    def visit_coordinate(self, node, visited_children):
        x, _, y, _ = visited_children
        return (x, y)

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = path+
        path = coordinate+ "\n"?
        coordinate = integer "," integer " -> "?
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def coorinate_bounds(data):
    min_x = math.inf
    min_y = math.inf
    max_x = -math.inf
    max_y = -math.inf

    for path in data:
        for x, y in path:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    return ((min_x, min_y), (max_x, max_y))


def input_to_grid(data, shape=(200, 1000)):
    grid = np.zeros(shape, dtype=np.int8)

    for path in data:
        prev_coordinate = None

        for coordinate in path:
            if prev_coordinate:
                plot_line(grid, prev_coordinate, coordinate)

            prev_coordinate = coordinate

    return grid


def plot_line(grid, start, end):
    start_x, start_y = start
    end_x, end_y = end

    x_direction = 1 if start_x <= end_x else -1
    y_direction = 1 if start_y <= end_y else -1

    for y in range(start_y, end_y + y_direction, y_direction):
        for x in range(start_x, end_x + x_direction, x_direction):
            grid[y, x] = 1


def drop_sand(grid, coordinate):
    x, y = coordinate

    if grid[y, x] != 0:
        return None

    while True:
        if y >= grid.shape[0] - 1:
            break

        if grid[y + 1, x] == 0:
            y += 1
        elif grid[y + 1, x - 1] == 0:
            y += 1
            x -= 1
        elif grid[y + 1, x + 1] == 0:
            y += 1
            x += 1
        else:
            break

    return (x, y)


def part1(data):
    """Solve part 1."""
    _, max_coordinate = coorinate_bounds(data)
    grid = input_to_grid(data, (max_coordinate[1] + 1, 1000))

    while True:
        sand_x, sand_y = drop_sand(grid, (500, 0))

        if sand_y == grid.shape[0] - 1:
            break

        grid[sand_y, sand_x] = 2

    return np.sum(grid == 2)


def part2(data):
    """Solve part 2."""
    _, max_coordinate = coorinate_bounds(data)
    grid = input_to_grid(data, (max_coordinate[1] + 2, 1000))

    while sand_coordinate := drop_sand(grid, (500, 0)):
        sand_x, sand_y = sand_coordinate
        grid[sand_y, sand_x] = 2

    return np.sum(grid == 2)


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
