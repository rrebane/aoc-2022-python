"""AoC 7, 2022."""

# Standard library imports
import pathlib
import sys

from parsimonious.grammar import Grammar, NodeVisitor


class InputVisitor(NodeVisitor):
    def visit_input(self, node, visited_children):
        _, commands = visited_children
        return [sublist[0] for sublist in commands]

    def visit_cd(self, node, visited_children):
        _, name, _ = visited_children
        return ("cd", name)

    def visit_ls(self, node, visited_children):
        _, dirs_and_files = visited_children
        return (
            "list",
            [sublist[0] for sublist in dirs_and_files],
        )

    def visit_dir(self, node, visited_children):
        _, name, _ = visited_children
        return ("dir", name)

    def visit_file(self, node, visited_children):
        size, _, name, _ = visited_children
        return ("file", name, size)

    def visit_name(self, node, visited_children):
        return node.text

    def visit_integer(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = "$ cd /\n" (cd / ls)+
        cd = "$ cd " name "\n"?
        ls = "$ ls\n" (dir / file)+
        dir = "dir " name "\n"?
        file = integer " " name "\n"?
        name = ~r"[a-z.]+"
        integer = ~r"[1-9][0-9]*"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return parse_file_tree(typed_input)


def parse_file_tree(data):
    root_dir = {}
    current_dir = [root_dir]

    for command in data:
        match command:
            case ("cd", dirname):
                if dirname == "..":
                    current_dir.pop()
                else:
                    current_dir.append(current_dir[-1][dirname])
            case ("list", nodes):
                for node in nodes:
                    match node:
                        case ("dir", dirname):
                            current_dir[-1][dirname] = {}
                        case ("file", filename, size):
                            current_dir[-1][filename] = size

    return root_dir


def node_size(node, dir_sizes={}, current_dir=[]):
    size = 0

    for name, val in node.items():
        if isinstance(val, dict):
            size += node_size(val, dir_sizes, current_dir.copy() + [name])
        else:
            size += val

    dirname = f"/{'/'.join(current_dir)}"
    dir_sizes[dirname] = size

    return size


def part1(data):
    """Solve part 1."""
    total_size = 0

    dir_sizes = {}
    _ = node_size(data, dir_sizes)

    for dirname, size in dir_sizes.items():
        if size <= 100000:
            total_size += size

    return total_size


def part2(data):
    """Solve part 2."""
    dir_sizes = {}
    current_size = node_size(data, dir_sizes)

    min_space_to_delete = 30000000 - (70000000 - current_size)

    eligible_dir_sizes = []

    for size in dir_sizes.values():
        if size >= min_space_to_delete:
            eligible_dir_sizes.append(size)

    return sorted(eligible_dir_sizes)[0]


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
