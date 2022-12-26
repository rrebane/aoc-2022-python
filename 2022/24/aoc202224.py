"""AoC 24, 2022."""

import heapq
import pathlib
import sys

import numpy as np

from parsimonious.grammar import Grammar, NodeVisitor

NEXT_STATE = {
    0: 0,
    1: np.array(
        [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    2: np.array(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    4: np.array(
        [
            [0, 0, 0],
            [4, 0, 0],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    8: np.array(
        [
            [0, 0, 0],
            [0, 0, 8],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    3: np.array(
        [
            [0, 1, 0],
            [0, 0, 0],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    5: np.array(
        [
            [0, 1, 0],
            [4, 0, 0],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    9: np.array(
        [
            [0, 1, 0],
            [0, 0, 8],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    6: np.array(
        [
            [0, 0, 0],
            [4, 0, 0],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    10: np.array(
        [
            [0, 0, 0],
            [0, 0, 8],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    12: np.array(
        [
            [0, 0, 0],
            [4, 0, 8],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    7: np.array(
        [
            [0, 1, 0],
            [4, 0, 0],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    11: np.array(
        [
            [0, 1, 0],
            [0, 0, 8],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    13: np.array(
        [
            [0, 1, 0],
            [4, 0, 8],
            [0, 0, 0],
        ],
        dtype=np.int8,
    ),
    14: np.array(
        [
            [0, 0, 0],
            [4, 0, 8],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
    15: np.array(
        [
            [0, 1, 0],
            [4, 0, 8],
            [0, 2, 0],
        ],
        dtype=np.int8,
    ),
}


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
        grid_cell = "." / "#" / "<" / ">" / "^" / "v"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def grid_size(data):
    return (len(data) - 2, len(data[0]) - 2)


def input_to_grid(data):
    n_rows = len(data) - 2
    n_cols = len(data[0]) - 2

    grid = np.zeros((n_rows, n_cols), dtype=np.int8)

    for y in range(n_rows):
        for x in range(n_cols):
            match data[y + 1][x + 1]:
                case "^":
                    grid[y, x] = 1
                case "v":
                    grid[y, x] = 2
                case "<":
                    grid[y, x] = 4
                case ">":
                    grid[y, x] = 8

    return grid


def next_grid(grid):
    new_grid = np.zeros((grid.shape[0] + 2, grid.shape[1] + 2), dtype=np.int8)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            new_grid[y : y + 3, x : x + 3] += NEXT_STATE[grid[y, x]]

    # Wrap around
    new_grid[1, :] += new_grid[new_grid.shape[0] - 1, :]
    new_grid[new_grid.shape[0] - 2, :] += new_grid[0, :]
    new_grid[:, 1] += new_grid[:, new_grid.shape[1] - 1]
    new_grid[:, new_grid.shape[1] - 2] += new_grid[:, 0]

    return new_grid[1:-1, 1:-1]


def neighbors(grid, pos):
    x_max = grid.shape[2] - 1
    y_max = grid.shape[1] - 1

    x, y, z = pos

    match (pos[0], pos[1]):
        case (0, -1):
            # Start
            return [(0, 0, z + 1), (0, -1, z + 1)]
        case (x, y) if x == x_max and y == y_max + 1:
            # Goal
            return [(x_max, y_max, z + 1), (x_max, y_max - 1, z + 1)]
        case (0, 0):
            # Next to start
            return [(1, 0, z + 1), (0, 1, z + 1), (0, 0, z + 1), (0, -1, z + 1)]
        case (x, 0) if x == x_max:
            return [(x_max - 1, 0, z + 1), (x_max, 1, z + 1), (x_max, 0, z + 1)]
        case (0, y) if y == y_max:
            return [(1, y_max, z + 1), (0, y_max - 1, z + 1), (0, y_max, z + 1)]
        case (x, y) if x == x_max and y == y_max:
            # Next to goal
            return [
                (x_max - 1, y_max, z + 1),
                (x_max, y_max - 1, z + 1),
                (x_max, y_max + 1, z + 1),
            ]
        case (0, y):
            return [(1, y, z + 1), (0, y - 1, z + 1), (0, y + 1, z + 1), (0, y, z + 1)]
        case (x, 0):
            return [(x - 1, 0, z + 1), (x + 1, 0, z + 1), (x, 1, z + 1), (x, 0, z + 1)]
        case (x, y) if x == x_max:
            return [
                (x_max - 1, y, z + 1),
                (x_max, y - 1, z + 1),
                (x_max, y + 1, z + 1),
                (x_max, y, z + 1),
            ]
        case (x, y) if y == y_max:
            return [
                (x - 1, y_max, z + 1),
                (x + 1, y_max, z + 1),
                (x, y_max - 1, z + 1),
                (x, y_max, z + 1),
            ]
        case (x, y):
            return [
                (x - 1, y, z + 1),
                (x + 1, y, z + 1),
                (x, y - 1, z + 1),
                (x, y + 1, z + 1),
                (x, y, z + 1),
            ]


def dijkstra(grid, target, state):
    dist, queue, visited = state

    target_pos = None

    while len(queue) > 0:
        _, pos = heapq.heappop(queue)
        visited.add(pos)

        if pos[0] == target[0] and pos[1] == target[1]:
            target_pos = pos
            break

        for neighbor_pos in neighbors(grid, pos):
            n_x, n_y, n_z = neighbor_pos

            if n_z >= grid.shape[0]:
                continue

            if (
                not (n_x == 0 and n_y == -1)
                and not (n_x == grid.shape[2] - 1 and n_y == grid.shape[1])
                and grid[n_z, n_y, n_x] != 0
            ):
                continue

            if not neighbor_pos in visited:
                neighbor_dist = dist[pos] + 1

                if neighbor_pos in dist:
                    if neighbor_dist < dist[neighbor_pos]:
                        dist[neighbor_pos] = neighbor_dist
                        heapq.heappush(queue, (neighbor_dist, neighbor_pos))
                else:
                    dist[neighbor_pos] = neighbor_dist
                    heapq.heappush(queue, (neighbor_dist, neighbor_pos))

    distance_to_target = dist[target_pos] if not target_pos is None else np.inf

    return distance_to_target, (dist, queue, visited)


def find_path(grid, start, target, max_steps=500):
    history = np.empty((max_steps + 1, grid.shape[0], grid.shape[1]), dtype=np.int8)
    history[0, :, :] = grid.copy()

    step = 0
    distance = np.inf

    dijkstra_state = (
        {(start[0], start[1], 0): 0},  # dist
        [(0, (start[0], start[1], 0))],  # queue
        set(),  # visited
    )

    while distance == np.inf and step < max_steps:
        step += 1
        history[step, :, :] = next_grid(history[step - 1, :, :])

        distance, dijkstra_state = dijkstra(
            history[0 : step + 1, :, :], target, dijkstra_state
        )

        # Re-add the positions from the final state to the search queue
        dist, queue, visited = dijkstra_state
        queue = [(d, (x, y, z)) for (x, y, z), d in dist.items() if z >= step]
        heapq.heapify(queue)
        dijkstra_state = dist, queue, visited

    return distance, history[step, :, :]


def part1(data):
    """Solve part 1."""
    grid = input_to_grid(data)
    distance, _ = find_path(grid, (0, -1), (grid.shape[1] - 1, grid.shape[0]))
    return distance


def part2(data):
    """Solve part 2."""
    grid = input_to_grid(data)
    start = (0, -1)
    goal = (grid.shape[1] - 1, grid.shape[0])
    distance1, grid = find_path(grid, start, goal)
    distance2, grid = find_path(grid, goal, start)
    distance3, grid = find_path(grid, start, goal)
    return distance1 + distance2 + distance3


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
