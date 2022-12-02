from __future__ import annotations
from dataclasses import dataclass
from typing import *
from pathlib import Path

WIN_SCORE = 6
DRAW_SCORE = 3
LOSS_SCORE = 0


WINNING_CASES = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper",
}

LOSING_CASES = {
    value: key for key, value in WINNING_CASES.items()
}


class Round:
    def get_your_move(self) -> str:
        raise NotImplementedError
    
    def is_won(self) -> bool:
        raise NotImplementedError

    def is_draw(self) -> bool:
        raise NotImplementedError


MOVES_MAPPING = {
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors",
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
}

@dataclass
class RoundPart1(Round):
    opponents_move: str
    your_move: str

    def __post_init__(self):
        self.opponents_move = MOVES_MAPPING.get(self.opponents_move, self.opponents_move)
        self.your_move = MOVES_MAPPING.get(self.your_move, self.your_move)

    def get_your_move(self) -> str:
        return self.your_move

    def is_won(self) -> bool:
        return (self.your_move, self.opponents_move) in list(WINNING_CASES.items())

    def is_draw(self) -> bool:
        return self.opponents_move == self.your_move


@dataclass
class RoundPart2(Round):
    opponents_move: str
    match_result: str

    def __post_init__(self):
        self.opponents_move = MOVES_MAPPING.get(self.opponents_move, self.opponents_move)

    def get_your_move(self) -> str:
        if self.is_won():
            return LOSING_CASES[self.opponents_move]
        if self.is_draw():
            return self.opponents_move
        return WINNING_CASES[self.opponents_move]
    
    def is_won(self) -> bool:
        return self.match_result == "Z"

    def is_draw(self) -> bool:
        return self.match_result == "Y"


def run_puzzle(filename: str, part: int):
    """
    Runs today's puzzle.
    """
    FOLDER = Path(__file__).parent
    puzzle_lines = read_puzzle_lines(FOLDER / filename)
    puzzle_content = parse_puzzle_lines(puzzle_lines, part=part)
    result = compute_solution(puzzle_content)
    print(f"The result for part {part} is {result}")


def read_puzzle_lines(filepath: Path) -> Iterator[str]:
    """
    Reads the AOC puzzle input.
    """
    with open(filepath, "r") as puzzle_file:
        yield from (line.strip() for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str], part: int = 1) -> List[Round]:
    round_type = RoundPart1 if part == 1 else RoundPart2
    return [
        round_type(opponents_move, your_move)
        for opponents_move, your_move in
        (line.split(" ") for line in lines)
    ]


def compute_solution(rounds: List[Round]) -> Any:
    return sum(compute_round_score(round) for round in rounds)


def compute_round_score(round: Round) -> int:
    return compute_win_score(round) + compute_shape_score(round.get_your_move())

def compute_win_score(round: Round) -> int:
    if round.is_won():
        return WIN_SCORE
    elif round.is_draw():
        return DRAW_SCORE
    return LOSS_SCORE

def compute_shape_score(move: str) -> int:
    return ["Rock", "Paper", "Scissors"].index(move) + 1

if __name__ == '__main__':
    run_puzzle("sample_input.txt", part=1)
    run_puzzle("input.txt", part=1)

    run_puzzle("sample_input.txt", part=2)
    run_puzzle("input.txt", part=2)
