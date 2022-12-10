"""AoC 10, 2022."""

import numpy as np
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_input(self, node, visited_children):
        return [inst for sublist in visited_children for inst in sublist]

    def visit_noop(self, node, visited_children):
        return ("noop",)

    def visit_addx(self, node, visited_children):
        _, integer, _ = visited_children
        return ("addx", integer)

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = (noop / addx)+
        noop = "noop" "\n"?
        addx = "addx " integer "\n"?
        integer = ~r"-?[1-9][0-9]*"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def instructions_to_reg_history(instructions):
    reg = [1]

    for instruction in instructions:
        match instruction:
            case ("noop",):
                reg.append(reg[-1])
            case ("addx", integer):
                reg.append(reg[-1])
                reg.append(reg[-1] + integer)

    return reg


def part1(data):
    """Solve part 1."""
    reg_x = instructions_to_reg_history(data)
    signals = [(pos + 1) * reg for pos, reg in enumerate(reg_x)]
    return np.sum(signals[19::40])


def print_screen(screen):
    printed_rows = []
    for row in screen:
        row_str = "".join(["#" if pixel == 1 else "." for pixel in row])
        printed_rows.append(row_str)

    return "\n".join(printed_rows)


def part2(data):
    """Solve part 2."""
    reg_x = instructions_to_reg_history(data)
    screen = np.zeros((6, 40), dtype=np.int8)

    for cycle, reg in enumerate(reg_x[:-1]):
        x = cycle % 40

        if x >= reg - 1 and x <= reg + 1:
            y = cycle // 40
            screen[y, x] = 1

    return print_screen(screen)


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
