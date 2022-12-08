"""AoC 8, 2022."""

import numpy as np
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_input(self, node, visited_children):
        grid_rows = visited_children
        return grid_rows

    def visit_grid_row(self, node, visited_children):
        digits, _ = visited_children
        return digits

    def visit_digit(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = grid_row+
        grid_row = digit+ "\n"?
        digit = ~r"[0-9]"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return np.array(typed_input, dtype=np.int8)


def part1(data):
    """Solve part 1."""
    visibility_grid = np.zeros(data.shape, dtype=np.int8)

    # Top
    for x in range(data.shape[1]):
        current_height = -1

        for y in range(data.shape[0]):
            if data[y, x] <= current_height:
                continue

            visibility_grid[y, x] = 1
            current_height = data[y, x]

    # Bottom
    for x in range(data.shape[1]):
        current_height = -1

        for y in range(data.shape[0] - 1, -1, -1):
            if data[y, x] <= current_height:
                continue

            visibility_grid[y, x] = 1
            current_height = data[y, x]

    # Left
    for y in range(data.shape[0]):
        current_height = -1

        for x in range(data.shape[1]):
            if data[y, x] <= current_height:
                continue

            visibility_grid[y, x] = 1
            current_height = data[y, x]

    # Right
    for y in range(data.shape[0]):
        current_height = -1

        for x in range(data.shape[1] - 1, -1, -1):
            if data[y, x] <= current_height:
                continue

            visibility_grid[y, x] = 1
            current_height = data[y, x]

    return visibility_grid.sum()


def tree_score(data, tree_y, tree_x):
    scores = np.array([0, 0, 0, 0], dtype=np.int32)
    tree_height = data[tree_y, tree_x]

    # Up
    for y in range(tree_y - 1, -1, -1):
        scores[0] += 1

        if data[y, tree_x] >= tree_height:
            break

    # Down
    for y in range(tree_y + 1, data.shape[0]):
        scores[1] += 1

        if data[y, tree_x] >= tree_height:
            break

    # Left
    for x in range(tree_x - 1, -1, -1):
        scores[2] += 1

        if data[tree_y, x] >= tree_height:
            break

    # Right
    for x in range(tree_x + 1, data.shape[1]):
        scores[3] += 1

        if data[tree_y, x] >= tree_height:
            break

    return scores.prod()


def part2(data):
    """Solve part 2."""
    tree_scores = np.zeros(data.shape, dtype=np.int32)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            tree_scores[y, x] = tree_score(data, y, x)

    return tree_scores.max()


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
