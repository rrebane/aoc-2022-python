"""AoC 2, 2022."""

# Standard library imports
import pathlib
import sys

from enum import Enum
from parsimonious.grammar import Grammar, NodeVisitor


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class InputVisitor(NodeVisitor):
    def visit_round(self, node, visited_children):
        opponent, _, you, _ = visited_children
        return [opponent, you]

    def visit_choice(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse_data(puzzle_input):
    """Parse input."""
    input_grammar = Grammar(
        r"""
        input = round+
        round = choice " "+ choice "\n"?
        choice = rock / paper / scissors
        rock = "A" / "X"
        paper = "B" / "Y"
        scissors = "C" / "Z"
        """
    )

    parsed_input = input_grammar.parse(puzzle_input)
    typed_input = InputVisitor().visit(parsed_input)

    return typed_input


def opponent_choice(choice):
    if choice == "A":
        return Choice.ROCK
    elif choice == "B":
        return Choice.PAPER
    elif choice == "C":
        return Choice.SCISSORS


def player_choice(choice):
    if choice == "X":
        return Choice.ROCK
    elif choice == "Y":
        return Choice.PAPER
    elif choice == "Z":
        return Choice.SCISSORS


def round_score(opponent, you):
    match [opponent, you]:
        case [Choice.ROCK, Choice.PAPER]:
            return 6
        case [Choice.ROCK, Choice.SCISSORS]:
            return 0
        case [Choice.PAPER, Choice.SCISSORS]:
            return 6
        case [Choice.PAPER, Choice.ROCK]:
            return 0
        case [Choice.SCISSORS, Choice.ROCK]:
            return 6
        case [Choice.SCISSORS, Choice.PAPER]:
            return 0
        case _:
            return 3


def choice_score(choice):
    return choice.value


def winning_choice(opponent):
    if opponent == Choice.ROCK:
        return Choice.PAPER
    elif opponent == Choice.PAPER:
        return Choice.SCISSORS
    else:
        return Choice.ROCK


def losing_choice(opponent):
    if opponent == Choice.ROCK:
        return Choice.SCISSORS
    elif opponent == Choice.PAPER:
        return Choice.ROCK
    else:
        return Choice.PAPER


def draw_choice(opponent):
    return opponent


def part1(data):
    """Solve part 1."""
    score = 0

    for opponent_input, player_input in data:
        opponent = opponent_choice(opponent_input)
        player = player_choice(player_input)
        score += round_score(opponent, player)
        score += choice_score(player)

    return score


def part2(data):
    """Solve part 2."""
    score = 0

    for opponent_input, player_input in data:
        opponent = opponent_choice(opponent_input)

        if player_input == "X":
            player = losing_choice(opponent)
        elif player_input == "Y":
            player = draw_choice(opponent)
        else:
            player = winning_choice(opponent)

        score += round_score(opponent, player)
        score += choice_score(player)

    return score


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
