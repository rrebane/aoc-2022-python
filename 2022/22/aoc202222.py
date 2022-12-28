"""AoC 22, 2022."""

import pathlib
import sys

from enum import Enum

import numpy as np

from parsimonious.grammar import Grammar, NodeVisitor


class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class InputVisitor(NodeVisitor):
    def visit_input(self, _node, visited_children):
        grid, _, instructions = visited_children
        return (grid, instructions)

    def visit_grid_row(self, _node, visited_children):
        grid_cells, _ = visited_children
        return grid_cells

    def visit_grid_cell(self, node, _visited_children):
        return node.text

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def visit_instructions(self, _node, visited_children):
        integer_or_direction = visited_children
        return [x for sublist in integer_or_direction for x in sublist]

    def visit_direction(self, node, _visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = grid "\n" instructions
        grid = grid_row+
        grid_row = grid_cell+ "\n"
        grid_cell = " " / "." / "#"
        instructions = (integer / direction)+
        integer = ~r"[0-9]+"
        direction = "L" / "R"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def input_to_grid(data):
    n_rows = len(data)
    n_cols = max(len(row) for row in data)

    grid = np.empty((n_rows, n_cols), dtype=np.int8)

    for y in range(n_rows):
        for x in range(n_cols):
            if x >= len(data[y]):
                grid[y, x] = 0
                continue

            match data[y][x]:
                case " ":
                    grid[y, x] = 0
                case ".":
                    grid[y, x] = 1
                case "#":
                    grid[y, x] = 2

    return grid


def input_to_path(data):
    instructions = []

    for instruction in data:
        match instruction:
            case int():
                instructions.append(instruction)
            case "L":
                instructions.append(Dir.LEFT)
            case "R":
                instructions.append(Dir.RIGHT)
            case _:
                assert False

    return instructions


def next_pos_in_direction(grid, pos, direction):
    x, y = pos

    match direction:
        case Dir.RIGHT:
            if (x + 1) >= grid.shape[1] or grid[y, x + 1] == 0:
                return (np.argmax(grid[y, :] > 0), y)
            return (x + 1, y)
        case Dir.DOWN:
            if (y + 1) >= grid.shape[0] or grid[y + 1, x] == 0:
                return (x, np.argmax(grid[:, x] > 0))
            return (x, y + 1)
        case Dir.LEFT:
            if (x - 1) < 0 or grid[y, x - 1] == 0:
                return (grid.shape[1] - 1 - np.argmax(grid[y, :][::-1] > 0), y)
            return (x - 1, y)
        case Dir.UP:
            if (y - 1) < 0 or grid[y - 1, x] == 0:
                return (x, grid.shape[0] - 1 - np.argmax(grid[:, x][::-1] > 0))
            return (x, y - 1)
        case _:
            assert False

    return (None, None)


def move(grid, pos, direction, steps):
    for _ in range(steps):
        (next_x, next_y) = next_pos_in_direction(grid, pos, direction)

        match grid[next_y, next_x]:
            case 1:
                pos = (next_x, next_y)
            case 2:
                break
            case _:
                assert False

    return pos


def turn(current, change):
    match change:
        case Dir.LEFT:
            return Dir((current.value - 1) % len(Dir))
        case Dir.RIGHT:
            return Dir((current.value + 1) % len(Dir))
        case _:
            assert False


def part1(data):
    """Solve part 1."""
    grid = input_to_grid(data[0])
    path = input_to_path(data[1])

    pos = (np.argmax(grid[0, :] == 1), 0)
    direction = Dir.RIGHT

    for instruction in path:
        match instruction:
            case int():
                pos = move(grid, pos, direction, instruction)
            case Dir():
                direction = turn(direction, instruction)

    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + direction.value


def grid_to_cube(grid):
    n_rows, n_cols = grid.shape
    face_size = np.gcd(n_rows, n_cols)

    face_bounds = []

    for y in range(0, n_rows, face_size):
        for x in range(0, n_cols, face_size):
            if grid[y, x] != 0:
                face_bounds.append(((x, y), (x + face_size, y + face_size)))

    assert len(face_bounds) == 6

    face_to_face = {k: {} for k in range(6)}

    for face in range(6):
        (b_min_x, b_min_y), _ = face_bounds[face]

        o_x, o_y = (b_min_x - face_size, b_min_y)
        o_face = pos_to_face(face_bounds, (o_x, o_y))
        if not o_face is None:
            face_to_face[face][Dir.LEFT] = (o_face, Dir.LEFT)

        o_x, o_y = (b_min_x + face_size, b_min_y)
        o_face = pos_to_face(face_bounds, (o_x, o_y))
        if not o_face is None:
            face_to_face[face][Dir.RIGHT] = (o_face, Dir.RIGHT)

        o_x, o_y = (b_min_x, b_min_y - face_size)
        o_face = pos_to_face(face_bounds, (o_x, o_y))
        if not o_face is None:
            face_to_face[face][Dir.UP] = (o_face, Dir.UP)

        o_x, o_y = (b_min_x, b_min_y + face_size)
        o_face = pos_to_face(face_bounds, (o_x, o_y))
        if not o_face is None:
            face_to_face[face][Dir.DOWN] = (o_face, Dir.DOWN)

    search_paths = [
        ([Dir.RIGHT, Dir.DOWN], Dir.DOWN, Dir.RIGHT),
        ([Dir.RIGHT, Dir.UP], Dir.UP, Dir.RIGHT),
        ([Dir.LEFT, Dir.DOWN], Dir.DOWN, Dir.LEFT),
        ([Dir.LEFT, Dir.UP], Dir.UP, Dir.LEFT),
        ([Dir.UP, Dir.LEFT], Dir.LEFT, Dir.UP),
        ([Dir.UP, Dir.RIGHT], Dir.RIGHT, Dir.UP),
        ([Dir.DOWN, Dir.LEFT], Dir.LEFT, Dir.DOWN),
        ([Dir.DOWN, Dir.RIGHT], Dir.RIGHT, Dir.DOWN),
    ]

    while not np.all(np.array([len(d) for d in face_to_face.values()]) >= 4):
        for face in range(6):
            for search_path in search_paths:
                path, start_dir, end_dir = search_path

                if start_dir in face_to_face[face]:
                    continue

                e_face = face
                dir_diff = 0

                for d in path:
                    adj_d = Dir((d.value + dir_diff) % len(Dir))
                    if adj_d in face_to_face[e_face]:
                        e_face, e_face_dir = face_to_face[e_face][adj_d]
                        dir_diff += e_face_dir.value - adj_d.value
                    else:
                        e_face = None
                        break

                if not e_face is None:
                    end_dir = Dir((end_dir.value + dir_diff) % len(Dir))
                    face_to_face[face][start_dir] = (e_face, end_dir)

    return (face_bounds, face_to_face)


def pos_to_face(face_bounds, pos):
    x, y = pos

    face = None

    for i, ((b_min_x, b_min_y), (b_max_x, b_max_y)) in enumerate(face_bounds):
        if b_min_x <= x < b_max_x and b_min_y <= y < b_max_y:
            face = i
            break

    return face


def edge_pos_to_corner_distance(cube_map, face, direction, pos):
    face_bounds, _ = cube_map
    (b_min_x, b_min_y), (b_max_x, b_max_y) = face_bounds[face]
    x, y = pos

    match direction:
        case Dir.RIGHT:
            return y - b_min_y
        case Dir.DOWN:
            return b_max_x - 1 - x
        case Dir.LEFT:
            return b_max_y - 1 - y
        case Dir.UP:
            return x - b_min_x
        case _:
            assert False

    return None


def corner_distance_to_edge_pos(cube_map, face, direction, dist):
    face_bounds, _ = cube_map
    (b_min_x, b_min_y), (b_max_x, b_max_y) = face_bounds[face]

    match direction:
        case Dir.RIGHT:
            return (b_min_x, b_min_y + dist)
        case Dir.DOWN:
            return (b_max_x - 1 - dist, b_min_y)
        case Dir.LEFT:
            return (b_max_x - 1, b_max_y - 1 - dist)
        case Dir.UP:
            return (b_min_x + dist, b_max_y - 1)
        case _:
            assert False

    return (None, None)


def next_cube_pos_in_direction(grid, cube_map, pos, direction):
    x, y = pos

    match direction:
        case Dir.RIGHT:
            next_x, next_y = (x + 1, y)
        case Dir.DOWN:
            next_x, next_y = (x, y + 1)
        case Dir.LEFT:
            next_x, next_y = (x - 1, y)
        case Dir.UP:
            next_x, next_y = (x, y - 1)
        case _:
            assert False

    face_bounds, face_to_face = cube_map
    face = pos_to_face(face_bounds, pos)
    (b_min_x, b_min_y), (b_max_x, b_max_y) = face_bounds[face]

    if not (b_min_x <= next_x < b_max_x and b_min_y <= next_y < b_max_y):
        next_face, next_direction = face_to_face[face][direction]
        dist = edge_pos_to_corner_distance(cube_map, face, direction, pos)
        next_pos = corner_distance_to_edge_pos(
            cube_map, next_face, next_direction, dist
        )
        return (next_pos, next_direction)

    return ((next_x, next_y), direction)


def move_cube(grid, cube_map, pos, direction, steps):
    for _ in range(steps):
        ((next_x, next_y), next_direction) = next_cube_pos_in_direction(
            grid, cube_map, pos, direction
        )

        match grid[next_y, next_x]:
            case 1:
                pos, direction = ((next_x, next_y), next_direction)
            case 2:
                break
            case _:
                assert False

    return pos, direction


def part2(data):
    """Solve part 2."""
    grid = input_to_grid(data[0])
    path = input_to_path(data[1])
    cube_map = grid_to_cube(grid)

    pos = (np.argmax(grid[0, :] == 1), 0)
    direction = Dir.RIGHT

    for instruction in path:
        match instruction:
            case int():
                pos, direction = move_cube(grid, cube_map, pos, direction, instruction)
            case Dir():
                direction = turn(direction, instruction)

    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + direction.value


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
