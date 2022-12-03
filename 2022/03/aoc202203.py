"""AoC 3, 2022."""

# Standard library imports
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_rucksack(self, node, visited_children):
        items, _ = visited_children
        return items.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = rucksack+
        rucksack = ~r"[a-zA-Z]+" "\n"?
        """)

    parsed_input = input_grammar.parse(puzzle_input)
    transformed_input = InputVisitor().visit(parsed_input)

    return transformed_input


def item_priority(item):
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 38


def rucksack_to_compartments(rucksack):
    num_items = len(rucksack)

    compartment1 = set(rucksack[0:num_items // 2])
    compartment2 = set(rucksack[num_items // 2:num_items])

    return (compartment1, compartment2)


def part1(data):
    """Solve part 1."""
    total_priority = 0

    for rucksack in data:
        compartment1, compartment2 = rucksack_to_compartments(rucksack)

        for item in compartment1:
            if item in compartment2:
                total_priority += item_priority(item)

    return total_priority


def part2(data):
    """Solve part 2."""
    total_priority = 0

    for i in range(0, len(data), 3):
        rucksack1 = set(data[i])
        rucksack2 = set(data[i + 1])
        rucksack3 = set(data[i + 2])

        common_items = rucksack1.intersection(rucksack2).intersection(rucksack3)

        total_priority += item_priority(common_items.pop())

    return total_priority


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
