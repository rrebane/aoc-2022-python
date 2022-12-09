"""AoC 9, 2022."""

# Standard library imports
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_instruction(self, node, visited_children):
        direction, _, count, _ = visited_children
        return (direction, count)

    def visit_direction(self, node, visited_children):
        return node.text

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = instruction+
        instruction = direction " " integer "\n"?
        direction = ("U" / "D" / "L" / "R")
        integer = ~r"[1-9][0-9]*"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def move_head(head, direction):
    head_x, head_y = head

    match direction:
        case "U":
            head_y -= 1
        case "D":
            head_y += 1
        case "L":
            head_x -= 1
        case "R":
            head_x += 1

    return (head_x, head_y)


def move_tail(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail

    diff_x = head_x - tail_x
    diff_y = head_y - tail_y

    match (abs(diff_x), abs(diff_y)):
        case (0, 2):
            tail_y += diff_y // 2
        case (2, 0):
            tail_x += diff_x // 2
        case (1, 2):
            tail_x += diff_x
            tail_y += diff_y // 2
        case (2, 1):
            tail_x += diff_x // 2
            tail_y += diff_y
        case (2, 2):
            tail_x += diff_x // 2
            tail_y += diff_y // 2
        case _:
            pass

    return (tail_x, tail_y)


def part1(data):
    """Solve part 1."""
    head = (0, 0)
    tail = (0, 0)
    trail = set()

    for instruction in data:
        direction, count = instruction

        for _ in range(count):
            head = move_head(head, direction)
            tail = move_tail(head, tail)
            trail.add(tail)

    return len(trail)


def part2(data, rope_len=10):
    """Solve part 2."""
    rope = [(0, 0) for _ in range(rope_len)]
    trail = set()

    for instruction in data:
        direction, count = instruction

        for _ in range(count):
            rope[0] = move_head(rope[0], direction)

            for i in range(1, rope_len):
                rope[i] = move_tail(rope[i - 1], rope[i])

            trail.add(rope[-1])

    return len(trail)


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
