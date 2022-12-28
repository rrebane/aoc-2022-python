"""AoC 16, 2022."""

from collections import deque
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


def distances(graph, source, targets):
    # https://en.wikipedia.org/wiki/Breadth-first_search
    dists = {source: 0}
    explored = {source}
    queue = deque([(0, source)])

    while len(queue) > 0:
        dist, u = queue.popleft()

        if all(target in dists for target in targets):
            break

        for v in graph[u]:
            if not v in explored:
                explored.add(v)
                dists[v] = dist + 1
                queue.append((dist + 1, v))

    return {k: v for k, v in dists.items() if k in targets}


def find_paths(
    graph,
    rates,
    source,
    n,
    visited,
    acc_pressure,
    acc_path,
    results,
):
    results.append((acc_pressure, acc_path))

    if all(dest in visited for dest in graph):
        return results

    for dest, dist in graph[source].items():
        if dest in visited:
            continue

        if dist + 1 > n:
            continue

        visited.add(dest)

        find_paths(
            graph,
            rates,
            dest,
            n - dist - 1,
            visited,
            acc_pressure + rates[dest] * (n - dist - 1),
            acc_path + [dest],
            results
        )

        visited.remove(dest)

    return results


def input_to_graph(data):
    graph = {id: edges for id, _, edges in data}
    rates = {id: rate for id, rate, _ in data}
    return graph, rates


def simplify_graph(graph, rates):
    points_of_interest = {id for id, rate in rates.items() if rate > 0}
    points_of_interest.add("AA")

    dists = {}

    for poi in points_of_interest:
        dists[poi] = distances(graph, poi, points_of_interest)

    return dists


def part1(data):
    """Solve part 1."""
    graph, rates = input_to_graph(data)
    dists = simplify_graph(graph, rates)
    paths = find_paths(dists, rates, "AA", 30, {"AA"}, 0, [], [])

    return sorted(paths, reverse=True)[0][0]


def part2(data):
    """Solve part 2."""
    graph, rates = input_to_graph(data)
    dists = simplify_graph(graph, rates)

    paths = find_paths(dists, rates, "AA", 26, {"AA"}, 0, [], [])
    sorted_paths = sorted(paths, reverse=True)

    paths_of_length = [[] for _ in range(len(dists))]

    for p in sorted_paths:
        path_len = len(p[1])
        paths_of_length[path_len].append(p)

    for i, paths in enumerate(paths_of_length):
        print(i, len(paths))

    max_pressure = 0
    lower_bound_cost = part1(data)

    for n in range(len(dists) // 2, 0, -1):
        len1 = n

        for len2 in range(len(dists) - len1 - 1, 0, -1):
            for c1, p1 in paths_of_length[len1]:
                for c2, p2 in paths_of_length[len2]:
                    if c1 + c2 < lower_bound_cost:
                        continue

                    if any(p in p2 for p in p1):
                        continue

                    max_pressure = max(max_pressure, c1 + c2)
                    lower_bound_cost = max_pressure

    return max_pressure


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
