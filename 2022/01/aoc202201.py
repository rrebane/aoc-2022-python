"""AoC 1, 2022."""

# Standard library imports
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor

input_grammar = Grammar(
    r"""
    input = elf+
    elf = (number "\n"?)+ "\n"?
    number = ~"[0-9]+"
    """
)


class InputVisitor(NodeVisitor):
    def visit_elf(self, node, visited_children):
        number_lines, _ = visited_children
        numbers = [number for number, _ in number_lines]
        return numbers

    def visit_number(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)
    return typed_input


def part1(data):
    """Solve part 1."""
    max_calories = 0

    for items in data:
        calories = sum(items)
        if calories > max_calories:
            max_calories = calories

    return max_calories


def part2(data):
    """Solve part 2."""
    return sum(sorted([sum(items) for items in data])[-3:])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
