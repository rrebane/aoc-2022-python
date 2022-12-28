"""AoC 21, 2022."""

import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_monkey(self, _node, visited_children):
        name, _, integer_or_operation, _ = visited_children
        return (name, integer_or_operation[0])

    def visit_operation(self, _node, visited_children):
        left, _, operand, _, right = visited_children
        return (operand, left, right)

    def visit_operand(self, node, _visited_children):
        return node.text

    def visit_name(self, node, _visited_children):
        return node.text

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = monkey+
        monkey = name ": " (integer / operation) "\n"?
        operation = name " " operand " " name
        operand = "+" / "-" / "*" / "/"
        name = ~r"[a-z]{4}"
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def input_to_dict(data):
    monkeys = {}

    for name, integer_or_operation in data:
        monkeys[name] = integer_or_operation

    return monkeys


def operation(operand, left, right):
    if left is None or right is None:
        return None

    match operand:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return left // right


def eval_monkey(monkeys, root_name):
    evaluated = {}

    queue = [root_name]

    while not root_name in evaluated:
        current_name = queue[-1]
        current_val = monkeys[current_name]

        match current_val:
            case int() | None:
                evaluated[current_name] = current_val
            case (operand, left, right):
                if not left in evaluated:
                    queue.append(left)
                if not right in evaluated:
                    queue.append(right)
                if not left in evaluated or not right in evaluated:
                    continue

                evaluated[current_name] = operation(
                    operand, evaluated[left], evaluated[right]
                )

        queue.pop()

    return evaluated


def part1(data):
    """Solve part 1."""
    monkeys = input_to_dict(data)
    evaluated = eval_monkey(monkeys, "root")
    return evaluated["root"]


def reduce(monkeys, evaluated, root_name):
    reduced = {}

    queue = [root_name]

    while len(queue) > 0:
        current_name = queue.pop()
        current_val = evaluated[current_name]

        if current_val is None:
            match monkeys[current_name]:
                case None:
                    reduced[current_name] = None
                case (operand, left, right):
                    if isinstance(evaluated[left], int):
                        left = evaluated[left]
                    else:
                        queue.append(left)

                    if isinstance(evaluated[right], int):
                        right = evaluated[right]
                    else:
                        queue.append(right)

                    reduced[current_name] = (operand, left, right)

    return reduced


def reduce_operation(result, operation):
    match operation:
        case ("=", left, right):
            assert result

            if isinstance(left, int):
                return (left, left)
            if isinstance(right, int):
                return (right, right)
        case ("+", left, right):
            if isinstance(left, int):
                return (left, result - left)
            if isinstance(right, int):
                return (result - right, right)
        case ("-", left, right):
            if isinstance(left, int):
                return (left, left - result)
            if isinstance(right, int):
                return (result + right, result)
        case ("*", left, right):
            if isinstance(left, int):
                return (left, result // left)
            if isinstance(right, int):
                return (result // right, right)
        case ("/", left, right):
            if isinstance(left, int):
                return (left, left // result)
            if isinstance(right, int):
                return (result * right, result)

    return (None, None)


def eval_unknown(monkeys, root_name):
    queue = [(root_name, True)]

    while len(queue) > 0:
        current_name, current_result = queue.pop()
        current_val = monkeys[current_name]

        match current_val:
            case (_, left, right):
                if isinstance(left, int):
                    _, right_val = reduce_operation(current_result, current_val)
                    queue.append((right, right_val))
                if isinstance(right, int):
                    left_val, _ = reduce_operation(current_result, current_val)
                    queue.append((left, left_val))
            case None:
                return current_result


def part2(data):
    """Solve part 2."""
    monkeys = input_to_dict(data)

    (_, root_left, root_right) = monkeys["root"]
    monkeys["root"] = ("=", root_left, root_right)
    monkeys["humn"] = None

    evaluated = eval_monkey(monkeys, "root")
    reduced = reduce(monkeys, evaluated, "root")
    return eval_unknown(reduced, "root")


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
