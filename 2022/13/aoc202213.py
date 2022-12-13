"""AoC 13, 2022."""

import functools
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_pair(self, node, visited_children):
        left, _, right, _ = visited_children
        return (left, right)

    def visit_packet(self, node, visited_children):
        packet = visited_children
        return packet[0]

    def visit_nonempty_packet(self, node, visited_children):
        _, integer_or_packet, _ = visited_children
        return integer_or_packet

    def visit_empty_packet(self, node, visited_children):
        return []

    def visit_integer_or_packet(self, node, visited_children):
        integer_or_packet, _ = visited_children
        return integer_or_packet[0]

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = pair+
        pair = packet "\n" packet "\n\n"?
        packet = nonempty_packet / empty_packet
        nonempty_packet = "[" integer_or_packet+ "]"
        empty_packet = "[]"
        integer_or_packet = (integer / packet) ","?
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def compare_packets(left, right):
    match (left, right):
        case (int(), int()):
            if left < right:
                return -1
            elif left > right:
                return 1
            else:
                return 0
        case (list(), int()):
            return compare_packets(left, [right])
        case (int(), list()):
            return compare_packets([left], right)
        case (list(), list()):
            for zl, zr in zip(left, right):
                comparison_result = compare_packets(zl, zr)

                if comparison_result == 0:
                    continue

                return comparison_result

            if len(left) < len(right):
                return -1
            elif len(left) > len(right):
                return 1
            else:
                return 0


def part1(data):
    """Solve part 1."""
    correct_pairs = []

    for i, pair in enumerate(data):
        left, right = pair
        if compare_packets(left, right) <= 0:
            correct_pairs.append(i + 1)

    return sum(correct_pairs)


def part2(data):
    """Solve part 2."""
    packets = [[[2]], [[6]]]

    for left, right in data:
        packets.append(left)
        packets.append(right)

    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare_packets))
    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


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
