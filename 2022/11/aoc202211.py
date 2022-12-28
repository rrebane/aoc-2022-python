"""AoC 11, 2022."""

# Standard library imports
import numpy as np
import pathlib
import sys

from dataclasses import dataclass
from parsimonious.grammar import Grammar, NodeVisitor
from typing import Callable, List
from util import profile_func


@dataclass
class Monkey:
    items: List[int]
    inspect_func: Callable[int, int]
    test_div: int
    if_true: int
    if_false: int


class InputVisitor(NodeVisitor):
    def visit_monkey(self, node, visited_children):
        _, _, _, items, operation, test, _ = visited_children
        return (items, operation, test)

    def visit_items(self, node, visited_children):
        _, items, _ = visited_children
        return items

    def visit_item(self, node, visited_children):
        integer, _ = visited_children
        return integer

    def visit_operation(self, node, visited_children):
        _, operator, _, operand, _ = visited_children
        return (operator, operand)

    def visit_operator(self, node, visited_children):
        return node.text

    def visit_operand(self, node, visited_children):
        if node.text == "old":
            return None

        [integer] = visited_children
        return integer

    def visit_test(self, node, visited_children):
        _, test_div, _, if_true, if_false = visited_children
        return (test_div, if_true, if_false)

    def visit_if_true(self, node, visited_children):
        _, integer, _ = visited_children
        return integer

    def visit_if_false(self, node, visited_children):
        _, integer = visited_children
        return integer

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = monkey+
        monkey = "Monkey " integer ":\n" items operation test "\n\n"?
        items = "  Starting items: " item+ "\n"
        item = integer ", "?
        operation = "  Operation: new = old " operator " " operand "\n"
        operator = "*" / "+"
        operand = integer / "old"
        test = "  Test: divisible by " integer "\n" if_true if_false
        if_true = "    If true: throw to monkey " integer "\n"
        if_false = "    If false: throw to monkey " integer
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def input_to_monkeys(data):
    monkeys = []

    for monkey in data:
        items, operation, test = monkey
        test_div, if_true, if_false = test
        monkeys.append(
            Monkey(
                np.array(items),
                operation_to_func(operation),
                test_div,
                if_true,
                if_false,
            )
        )

    return monkeys


def operation_to_func(operation):
    match operation:
        case ("*", None):
            return lambda a: a * a
        case ("+", None):
            return lambda a: a + a
        case ("*", operand):
            return lambda a: a * operand
        case ("+", operand):
            return lambda a: a + operand


def part1(data, num_rounds=20, relief_func=lambda x: np.floor_divide(x, 3)):
    """Solve part 1."""
    monkeys = input_to_monkeys(data)

    inspect_count = [0 for _ in range(len(monkeys))]

    for _ in range(num_rounds):
        for monkey_nr, monkey in enumerate(monkeys):
            inspect_count[monkey_nr] += len(monkey.items)
            items = relief_func(monkey.inspect_func(monkey.items))
            cond = np.mod(items, monkey.test_div) == 0

            monkeys[monkey.if_true].items = np.append(
                monkeys[monkey.if_true].items, items[cond]
            )

            monkeys[monkey.if_false].items = np.append(
                monkeys[monkey.if_false].items, items[~cond]
            )

            monkey.items = np.empty(0)

    inspect_count.sort(reverse=True)

    return inspect_count[0] * inspect_count[1]


def part2(data):
    """Solve part 2."""
    monkeys = input_to_monkeys(data)

    relief_mod = 1

    for monkey in monkeys:
        relief_mod *= monkey.test_div

    return part1(data, num_rounds=10000, relief_func=lambda x: np.mod(x, relief_mod))


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
