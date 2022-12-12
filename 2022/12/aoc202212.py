"""AoC 12, 2022."""

import heapq
import math
import numpy as np
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_grid_row(self, node, visited_children):
        cells, _ = visited_children
        return cells

    def visit_grid_cell(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = grid_row+
        grid_row = grid_cell+ "\n"?
        grid_cell = ~r"[a-z]" / "S" / "E"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def input_to_grid(data):
    nrows = len(data)
    ncols = len(data[0])

    start_pos = (0, 0)
    end_pos = (0, 0)
    grid = np.empty((nrows, ncols), dtype=np.int8)

    for y in range(nrows):
        for x in range(ncols):
            match data[y][x]:
                case "S":
                    start_pos = (x, y)
                    grid[y, x] = ord("a") - 97
                case "E":
                    end_pos = (x, y)
                    grid[y, x] = ord("z") - 97
                case cell:
                    grid[y, x] = ord(cell) - 97

    return (grid, start_pos, end_pos)


def neighbor_positions(grid, pos):
    x_max = grid.shape[1] - 1
    y_max = grid.shape[0] - 1

    match pos:
        case (0, 0):
            return [(1, 0), (0, 1)]
        case (x, 0) if x == x_max:
            return [(x_max - 1, 0), (x_max, 1)]
        case (0, y) if y == y_max:
            return [(1, y_max), (0, y_max - 1)]
        case (x, y) if x == x_max and y == y_max:
            return [(x_max - 1, y_max), (x_max, y_max - 1)]
        case (0, y):
            return [(1, y), (0, y - 1), (0, y + 1)]
        case (x, 0):
            return [(x - 1, 0), (x + 1, 0), (x, 1)]
        case (x, y) if x == x_max:
            return [(x_max - 1, y), (x_max, y - 1), (x_max, y + 1)]
        case (x, y) if y == y_max:
            return [(x - 1, y_max), (x + 1, y_max), (x, y_max - 1)]
        case (x, y):
            return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def dijkstra(grid, start_pos, targets, neighbor_cond_func):
    dist = {
        (x, y): math.inf for y in range(grid.shape[0]) for x in range(grid.shape[1])
    }
    dist[start_pos] = 0
    queue = [(0, start_pos)]
    visited = set()

    while len(queue) > 0:
        _, pos = heapq.heappop(queue)
        visited.add(pos)

        pos_x, pos_y = pos

        for neighbor_pos in neighbor_positions(grid, pos):
            neighbor_x, neighbor_y = neighbor_pos

            if not neighbor_cond_func(grid[neighbor_y, neighbor_x], grid[pos_y, pos_x]):
                continue

            if not neighbor_pos in visited:
                neighbor_dist = dist[pos] + 1

                if neighbor_dist < dist[neighbor_pos]:
                    dist[neighbor_pos] = neighbor_dist
                    heapq.heappush(queue, (neighbor_dist, neighbor_pos))

    shortest_dist_to_target = math.inf

    for target_pos in targets:
        if dist[target_pos] < shortest_dist_to_target:
            shortest_dist_to_target = dist[target_pos]

    return shortest_dist_to_target


def part1(data):
    """Solve part 1."""
    grid, start_pos, end_pos = input_to_grid(data)
    neighbor_cond_func = lambda a, b: a <= b + 1
    return dijkstra(grid, start_pos, set([end_pos]), neighbor_cond_func)


def part2(data):
    """Solve part 2."""
    grid, _, end_pos = input_to_grid(data)
    zero_ys, zero_xs = np.where(grid == 0)
    start_positions = set(zip(zero_xs, zero_ys))
    neighbor_cond_func = lambda a, b: a >= b - 1
    return dijkstra(grid, end_pos, start_positions, neighbor_cond_func)


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
