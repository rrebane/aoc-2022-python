"""AoC 5, 2022."""

# Standard library imports
import copy
import pathlib
import sys

from dataclasses import dataclass
from parsimonious.grammar import Grammar, NodeVisitor
from typing import List


@dataclass
class Data:
    stacks: List[List[str]]
    instructions: List[tuple[int, int, int]]


class InputVisitor(NodeVisitor):
    def visit_input(self, node, visited_children):
        crate_rows, stack_numbers, _, instructions = visited_children

        stacks = [[] for _ in range(len(stack_numbers))]

        for crate_row in crate_rows:
            for stack_number, crate in enumerate(crate_row):
                if crate:
                    stacks[stack_number].append(crate)

        for stack in stacks:
            stack.reverse()

        return Data(stacks, instructions)

    def visit_crate_row(self, node, visited_children):
        crates, _ = visited_children
        return [crate for sublist in crates for crate in sublist]

    def visit_crate(self, node, visited_children):
        _, label, _, _ = visited_children
        return label

    def visit_crate_label(self, node, visited_children):
        return node.text

    def visit_empty(self, node, visited_children):
        return None

    def visit_stack_numbers(self, node, visited_children):
        numbers, _ = visited_children
        return numbers

    def visit_stack_number(self, node, visited_children):
        _, number, _, _ = visited_children
        return number

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def visit_instruction(self, node, visited_children):
        _, count, _, start, _, end, _ = visited_children
        return (count, start - 1, end - 1)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = crate_row+ stack_numbers "\n" instruction+
        crate_row = (crate / empty)+ "\n"
        crate = "[" crate_label "]" " "?
        crate_label = ~r"[A-Z]"
        empty = "   " " "?
        stack_numbers = stack_number+ "\n"
        stack_number = " " integer " " " "?
        instruction = "move " integer " from " integer " to " integer "\n"?
        integer = ~r"[1-9][0-9]*"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def part1(data):
    """Solve part 1."""
    stacks = copy.deepcopy(data.stacks)

    for instruction in data.instructions:
        count, start, end = instruction

        for _ in range(count):
            stacks[end].append(stacks[start].pop())

    return "".join(stack[-1] for stack in stacks if len(stack) > 0)


def part2(data):
    """Solve part 2."""
    stacks = copy.deepcopy(data.stacks)

    for instruction in data.instructions:
        count, start, end = instruction

        stacks[end].extend(stacks[start][len(stacks[start]) - count :])
        stacks[start] = stacks[start][: len(stacks[start]) - count]

    return "".join(stack[-1] for stack in stacks if len(stack) > 0)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text())
        print("\n".join(str(solution) for solution in solutions))
