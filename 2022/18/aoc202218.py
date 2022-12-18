"""AoC 18, 2022."""

import numpy as np
import math
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_cube(self, _node, visited_children):
        x, _, y, _, z, _ = visited_children
        return (x, y, z)

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = cube+
        cube = integer "," integer "," integer "\n"?
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def grid_bounds(data):
    min_x = min_y = min_z = math.inf
    max_x = max_y = max_z = -math.inf

    for x, y, z in data:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

    return ((min_x, min_y, min_z), (max_x, max_y, max_z))


def neighbors(grid, cube):
    x, y, z = cube

    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def part1(data):
    """Solve part 1."""
    side_count = 0

    grid = set(data)

    for cube in grid:
        for neighbor in neighbors(grid, cube):
            if not neighbor in grid:
                side_count += 1

    return side_count


def is_in_bounds(cube, min_bounds, max_bounds):
    min_x, min_y, min_z = min_bounds
    max_x, max_y, max_z = max_bounds
    x, y, z = cube

    return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z


def part2(data):
    """Solve part 2."""
    side_count = 0

    grid_min, grid_max = grid_bounds(data)

    min_bounds = (grid_min[0] - 1, grid_min[1] - 1, grid_min[2] - 1)
    max_bounds = (grid_max[0] + 1, grid_max[1] + 1, grid_max[2] + 1)

    grid = set(data)

    queue = [min_bounds]
    explored = {min_bounds}

    while len(queue) > 0:
        cube = queue.pop()

        for neighbor in neighbors(grid, cube):
            if not is_in_bounds(neighbor, min_bounds, max_bounds):
                continue

            if neighbor in grid:
                side_count += 1
            elif not neighbor in explored:
                explored.add(neighbor)
                queue.append(neighbor)

    return side_count


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
