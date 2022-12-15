"""AoC 15, 2022."""

import math
import numpy as np
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_sensor(self, _node, visited_children):
        sensor_loc, _, beacon_loc, _ = visited_children
        return (sensor_loc, beacon_loc)

    def visit_sensor_location(self, _node, visited_children):
        _, x, _, y = visited_children
        return (x, y)

    def visit_beacon_location(self, _node, visited_children):
        _, x, _, y = visited_children
        return (x, y)

    def visit_integer(self, node, _visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    input_grammar = Grammar(
        r"""
        input = sensor+
        sensor = sensor_location ": " beacon_location "\n"?
        sensor_location = "Sensor at x=" integer ", y=" integer
        beacon_location = "closest beacon is at x=" integer ", y=" integer
        integer = ~r"-?[0-9]+"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def input_to_circles(data):
    circles = []

    for sensor_loc, beacon_loc in data:
        sensor_x, sensor_y = sensor_loc
        beacon_x, beacon_y = beacon_loc

        dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        circles.append((sensor_loc, dist))

    return circles


def input_to_locations(data):
    locations = set()

    for sensor_loc, beacon_loc in data:
        locations.add(sensor_loc)
        locations.add(beacon_loc)

    return locations


def circle_area_bounds(circles):
    min_x = math.inf
    min_y = math.inf
    max_x = -math.inf
    max_y = -math.inf

    for sensor_loc, radius in circles:
        sensor_x, sensor_y = sensor_loc

        min_x = min(min_x, sensor_x - radius)
        min_y = min(min_y, sensor_y - radius)
        max_x = max(max_x, sensor_x + radius)
        max_y = max(max_y, sensor_y + radius)

    return ((min_x, min_y), (max_x, max_y))


def is_location_within_circle(circle, target_loc):
    (circle_x, circle_y), circle_radius = circle
    target_x, target_y = target_loc

    dist = abs(circle_x - target_x) + abs(circle_y - target_y)

    return dist <= circle_radius


def part1(data, target_y):
    """Solve part 1."""
    circles = input_to_circles(data)
    known_locations = input_to_locations(data)
    min_loc, max_loc = circle_area_bounds(circles)

    excluded_loc_count = 0

    for target_x in range(min_loc[0], max_loc[0] + 1):
        target_loc = (target_x, target_y)

        if target_loc in known_locations:
            continue

        for circle in circles:
            if is_location_within_circle(circle, target_loc):
                excluded_loc_count += 1
                break

    return excluded_loc_count


def location_to_location_distance(p1, p2):
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def diag_line_intersection(a1, b1, a2, b2):
    x = (b2 - b1) // (a1 - a2)
    y = a1 * x + b1
    return (x, y)


def circle_corners(circle):
    (c_x, c_y), c_r = circle

    return [
        (c_x - c_r, c_y),
        (c_x, c_y - c_r),
        (c_x + c_r, c_y),
        (c_x, c_y + c_r),
    ]


def circle_edges(circle):
    corners = circle_corners(circle)

    return [
        (1, (corners[0][1] - corners[0][0])),
        (-1, (corners[1][1] + corners[1][0])),
        (1, (corners[2][1] - corners[2][0])),
        (-1, (corners[3][1] + corners[3][0])),
    ]


def circle_intersections(c1, c2):
    c1_loc, c1_r = c1
    c2_loc, c2_r = c2

    c_to_c_dist = location_to_location_distance(c1_loc, c2_loc)

    # Circles are disjoint
    if c_to_c_dist >= c1_r + c2_r:
        return []

    # Circles are entirely overlapping
    if c_to_c_dist + c1_r <= c2_r or c_to_c_dist + c2_r <= c1_r:
        return []

    # Circles are partially overlapping
    c1_edges = circle_edges(c1)
    c2_edges = circle_edges(c2)

    intersections = set()

    for c1_edge_a, c1_edge_b in c1_edges:
        for c2_edge_a, c2_edge_b in c2_edges:
            if c1_edge_a == c2_edge_a:
                continue

            intersection = diag_line_intersection(c1_edge_a, c1_edge_b, c2_edge_a, c2_edge_b)

            c1_to_i_dist = location_to_location_distance(c1_loc, intersection)
            c2_to_i_dist = location_to_location_distance(c2_loc, intersection)

            if c1_to_i_dist <= c1_r and c2_to_i_dist <= c2_r:
                intersections.add(intersection)

    return intersections


def is_location_in_bounds(loc, bounds):
    bounds_min, bounds_max = bounds
    min_x, min_y = bounds_min
    max_x, max_y = bounds_max
    x, y = loc

    if x < min_x or x > max_x:
        return False

    if y < min_y or y > max_y:
        return False

    return True


def nearby_locations(loc):
    x, y = loc
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            yield (x + i, y + j)


def is_location_within_any_circle(circles, target_loc):
    for circle in circles:
        if is_location_within_circle(circle, target_loc):
            return True

    return False


def part2(data, search_bounds):
    """Solve part 2."""
    circles = input_to_circles(data)

    intersections = set()
    num_circles = len(circles)

    for i in range(num_circles - 1):
        for j in range(i + 1, num_circles):
            intersections.update(circle_intersections(circles[i], circles[j]))

    distress_beacon_loc = None

    for intersection_loc in intersections:
        for candidate_loc in nearby_locations(intersection_loc):
            if not is_location_in_bounds(candidate_loc, search_bounds):
                continue

            if not is_location_within_any_circle(circles, candidate_loc):
                distress_beacon_loc = candidate_loc
                break

        if distress_beacon_loc:
            break

    distress_beacon_x, distress_beacon_y = distress_beacon_loc

    return distress_beacon_x * 4000000 + distress_beacon_y


def solve(puzzle_input, puzzle_param):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    part1_param, part2_param = puzzle_param
    yield part1(data, part1_param)
    yield part2(data, part2_param)


def get_input_param(path):
    match path:
        case "example1.txt":
            return (10, ((0, 0), (20, 20)))
        case "input.txt":
            return (2000000, ((0, 0), (4000000, 4000000)))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(
            puzzle_input=pathlib.Path(path).read_text().rstrip(),
            puzzle_param=get_input_param(path),
        )
        print("\n".join(str(solution) for solution in solutions))
