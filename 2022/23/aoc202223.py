"""AoC 23, 2022."""

import math
import pathlib
import sys

from enum import Enum

import numpy as np

from parsimonious.grammar import Grammar, NodeVisitor


class Dir(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


class InputVisitor(NodeVisitor):
    def visit_grid_row(self, _node, visited_children):
        grid_cells, _ = visited_children
        return grid_cells

    def visit_grid_cell(self, node, _visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = grid_row+
        grid_row = grid_cell+ "\n"?
        grid_cell = "." / "#"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def grid_bounds(grid):
    min_x = min_y = math.inf
    max_x = max_y = -math.inf

    for x, y in grid:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return ((min_x, min_y), (max_x + 1, max_y + 1))


def adjacent_pos(pos, direction):
    x, y = pos

    match direction:
        case Dir.NORTH:
            return [
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
            ]
        case Dir.SOUTH:
            return [
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            ]
        case Dir.WEST:
            return [
                (x - 1, y - 1),
                (x - 1, y),
                (x - 1, y + 1),
            ]
        case Dir.EAST:
            return [
                (x + 1, y - 1),
                (x + 1, y),
                (x + 1, y + 1),
            ]
        case None:
            return [
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
                (x - 1, y - 1),
                (x - 1, y),
                (x - 1, y + 1),
                (x + 1, y - 1),
                (x + 1, y),
                (x + 1, y + 1),
            ]

        case _:
            assert False


def move_in_direction(pos, direction):
    x, y = pos

    match direction:
        case Dir.NORTH:
            return (x, y - 1)
        case Dir.SOUTH:
            return (x, y + 1)
        case Dir.WEST:
            return (x - 1, y)
        case Dir.EAST:
            return (x + 1, y)
        case _:
            assert False

    return (None, None)


def input_to_grid(data):
    grid = set()

    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "#":
                grid.add((x, y))

    return grid


def simulate(grid, max_rounds):
    initial_direction = Dir.NORTH
    n_rounds = 0

    while True:
        next_grid = {}
        n_moves = 0

        for pos in grid:
            next_pos = pos

            if any(adj_pos in grid for adj_pos in adjacent_pos(pos, None)):
                for i in range(4):
                    direction = Dir((initial_direction.value + i) % len(Dir))

                    if not any(
                        adj_pos in grid for adj_pos in adjacent_pos(pos, direction)
                    ):
                        next_pos = move_in_direction(pos, direction)
                        n_moves += 1
                        break

            if next_pos in next_grid:
                next_grid[next_pos].append(pos)
            else:
                next_grid[next_pos] = [pos]

        grid = set()

        for next_pos, prev_poss in next_grid.items():
            if len(prev_poss) > 1:
                for prev_pos in prev_poss:
                    grid.add(prev_pos)
            else:
                grid.add(next_pos)

        n_rounds += 1

        if n_rounds >= max_rounds or n_moves == 0:
            break

        initial_direction = Dir((initial_direction.value + 1) % len(Dir))

    return grid, n_rounds


def part1(data):
    """Solve part 1."""
    grid = input_to_grid(data)
    grid, _ = simulate(grid, 10)
    (g_min_x, g_min_y), (g_max_x, g_max_y) = grid_bounds(grid)
    return (g_max_x - g_min_x) * (g_max_y - g_min_y) - len(grid)


def part2(data):
    """Solve part 2."""
    grid = input_to_grid(data)
    _, n_rounds = simulate(grid, np.inf)
    return n_rounds


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
