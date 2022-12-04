"""AoC 4, 2022."""

# Standard library imports
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_pair(self, node, visited_children):
        section1, _, section2, _ = visited_children
        return (section1, section2)

    def visit_section(self, node, visited_children):
        number1, _, number2 = visited_children
        return (number1, number2)

    def visit_number(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = pair+
        pair = section "," section "\n"?
        section = number "-" number
        number = ~r"[1-9][0-9]*"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def part1(data):
    """Solve part 1."""
    overlapping_sections = 0

    for section1, section2 in data:
        s1_start, s1_end = section1
        s2_start, s2_end = section2

        if s1_start <= s2_start and s1_end >= s2_end:
            overlapping_sections += 1
        elif s2_start <= s1_start and s2_end >= s1_end:
            overlapping_sections += 1

    return overlapping_sections


def part2(data):
    """Solve part 2."""
    distinct_sections = 0

    for section1, section2 in data:
        s1_start, s1_end = section1
        s2_start, s2_end = section2

        if s1_end < s2_start or s2_end < s1_start:
            distinct_sections += 1
        elif s1_start > s2_end or s2_start > s1_end:
            distinct_sections += 1

    return len(data) - distinct_sections


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
