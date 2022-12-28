"""AoC 19, 2022."""

import math
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor

import numpy as np


class InputVisitor(NodeVisitor):
    def visit_blueprint(self, _node, visited_children):
        _, _, _, ore, clay, obsidian, geode, _ = visited_children
        return (ore, clay, obsidian, geode)

    def visit_ore(self, _node, visited_children):
        _, ore, _ = visited_children
        return ore

    def visit_clay(self, _node, visited_children):
        _, ore, _ = visited_children
        return ore

    def visit_obsidian(self, _node, visited_children):
        _, ore, _, clay, _ = visited_children
        return (ore, clay)

    def visit_geode(self, _node, visited_children):
        _, ore, _, obsidian, _ = visited_children
        return (ore, obsidian)

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = blueprint+
        blueprint = "Blueprint " integer ": " ore clay obsidian geode "\n"?
        ore = "Each ore robot costs " integer " ore. "
        clay = "Each clay robot costs " integer " ore. "
        obsidian = "Each obsidian robot costs " integer " ore and " integer " clay. "
        geode = "Each geode robot costs " integer " ore and " integer " obsidian."
        integer = ~r"[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def t_until_next(costs, robots, resources):
    result = []

    for i in range(4):
        missing_resources = costs[i] - resources

        if np.all(missing_resources <= 0):
            result.append(0)
            continue

        mask = np.logical_and(costs[i] != 0, missing_resources > 0)

        result.append(
            np.array(
                [
                    int(np.ceil(a / b)) if b > 0 else np.inf
                    for a, b in zip(missing_resources[mask], robots[mask])
                ]
            ).max()
        )

    return result


def resource_bounds(costs, robots, resources, time):
    new_robots = np.zeros(4, np.int32)
    new_resources = resources.copy()

    for _ in range(time):
        new_resources += robots + new_robots

        for i in range(4):
            if np.all(new_resources - costs[i] * (new_robots[i] + 1) >= 0):
                new_robots[i] += 1

    return new_resources


def state_to_key(time, robots, resources):
    return (
        time,
        robots[0],
        robots[1],
        robots[2],
        robots[3],
        resources[0],
        resources[1],
        resources[2],
        resources[3],
    )


def simulate_blueprint(
    costs,
    time,
    memory,
    robots=np.array([1, 0, 0, 0], dtype=np.int32),
    resources=np.array([0, 0, 0, 0], dtype=np.int32),
    best=0,
):
    state_key = state_to_key(time, robots, resources)
    if state_key in memory:
        return memory[state_key]

    if time <= 0:
        return resources[3]

    max_geodes = max(resources[3] + robots[3] * time, best)

    t_until_resources = t_until_next(costs, robots, resources)
    limits = np.ceil((np.max(costs * time, axis=0) - resources) / time).astype(np.int32)

    for i, t_until_resource in list(enumerate(t_until_resources))[::-1]:
        if i != 3 and robots[i] >= limits[i]:
            continue

        if t_until_resource == np.inf:
            continue

        build_time = int(math.ceil(t_until_resource)) + 1

        if time - build_time < 0:
            continue

        new_robot = np.array([1 if n == i else 0 for n in range(4)], dtype=np.int32)

        upper_bounds = resource_bounds(
            costs,
            robots + new_robot,
            resources - costs[i] + robots * build_time,
            time - build_time,
        )

        if upper_bounds[3] < max_geodes:
            continue

        geodes = simulate_blueprint(
            costs,
            time - build_time,
            memory,
            robots + new_robot,
            resources - costs[i] + robots * build_time,
            max_geodes,
        )

        max_geodes = max(geodes, max_geodes)

    memory[state_key] = max_geodes

    return max_geodes


def blueprint_to_cost(blueprint):
    ore, clay, obsidian, geode = blueprint

    return np.array(
        [
            [ore, 0, 0, 0],
            [clay, 0, 0, 0],
            [obsidian[0], obsidian[1], 0, 0],
            [geode[0], 0, geode[1], 0],
        ],
        dtype=np.int32,
    )


def part1(data):
    """Solve part 1."""
    quality_levels = []

    for i, blueprint in enumerate(data):
        costs = blueprint_to_cost(blueprint)
        geodes = simulate_blueprint(costs, 24, {})
        quality_levels.append((i + 1) * geodes)

    return sum(quality_levels)


def part2(data):
    """Solve part 2."""
    bp_geodes = []

    for i, blueprint in enumerate(data[:3]):
        costs = blueprint_to_cost(blueprint)
        geodes = simulate_blueprint(costs, 32, {})
        bp_geodes.append(geodes)

    return np.prod(bp_geodes)


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
