"""AoC 16, 2022."""

import math
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_valve_and_tunnels(self, _node, visited_children):
        (tunnel_id, flow_rate), _, connected_tunnel_ids, _ = visited_children
        return (tunnel_id, flow_rate, connected_tunnel_ids)

    def visit_valve(self, _node, visited_children):
        _, id, _, flow_rate = visited_children
        return (id, flow_rate)

    def visit_tunnels(self, _node, visited_children):
        _, ids = visited_children
        return ids

    def visit_id_and_comma(self, _node, visited_children):
        id, _ = visited_children
        return id

    def visit_id(self, node, _visited_children):
        return node.text

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = valve_and_tunnels+
        valve_and_tunnels = valve "; " tunnels "\n"?
        valve = "Valve " id " has flow rate=" integer
        tunnels = ~r"tunnels? leads? to valves? " id_and_comma+
        id_and_comma = id ", "?
        id = ~r"[A-Z]+"
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def paths_of_length(
    graph,
    source,
    n,
    current_path=[],
    used_valves=set(),
    current_pressure=0,
    visited=set(),
):
    if n <= 0:
        return current_pressure

    weight, edges = graph[source]

    max_pressure = -math.inf

    if weight > 0 and not source in used_valves:
        used_valves.add(source)
        current_path.append(source)
        pressure = paths_of_length(
            graph,
            source,
            n - 1,
            current_path,
            used_valves,
            current_pressure + weight * (n - 1),
            set()
        )
        current_path.pop()
        used_valves.remove(source)

        if pressure > max_pressure:
            max_pressure = pressure

    for dest in edges:
        if dest in visited:
            continue

        visited.add(dest)
        current_path.append(dest)
        pressure = paths_of_length(
            graph, dest, n - 1, current_path, used_valves, current_pressure, visited
        )
        current_path.pop()
        visited.remove(dest)

        if pressure > max_pressure:
            max_pressure = pressure

    return max_pressure


def part1(data):
    """Solve part 1."""
    graph = {id: (weight, edges) for id, weight, edges in data}
    max_pressure = paths_of_length(graph, "AA", 30, ["AA"])
    return max_pressure


def part2(data):
    """Solve part 2."""


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
