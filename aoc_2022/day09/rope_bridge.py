from __future__ import annotations
from dataclasses import dataclass
from itertools import pairwise
from typing import *
from pathlib import Path


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def distance(self, other: Position) -> int:
        return sum([abs(self.x - other.x), abs(self.y - other.y)])

    def is_aligned_with(self, other: Position) -> bool:
        return self.x == other.x or self.y == other.y

    @staticmethod
    def midpoint(start: Position, end: Position) -> Position:
        return Position(x=(end.x + start.x) // 2, y=(end.y + start.y) // 2)


def run_puzzle(filename: str):
    """
    Runs today's puzzle.
    """
    FOLDER = Path(__file__).parent
    puzzle_lines = read_puzzle_lines(FOLDER / filename)
    puzzle_content = parse_puzzle_lines(puzzle_lines)
    result_one = solve_part_one(puzzle_content)
    print(f"The result for part 1 is {result_one}")
    result_two = solve_part_two(puzzle_content)
    print(f"The result for part 2 is {result_two}")


def read_puzzle_lines(filepath: Path) -> Iterator[str]:
    """
    Reads the AOC puzzle input.
    """
    with open(filepath, "r") as puzzle_file:
        yield from (line.strip() for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str]) -> List[Tuple[str, int]]:
    directions = (line.split(" ") for line in lines)
    return [(direction, int(distance)) for direction, distance in directions]


def solve_part_one(puzzle: List[Tuple[str, int]]) -> int:
    head, tail = Position(0, 0), Position(0, 0)
    tail_positions = [tail]
    for direction, distance in puzzle:
        for _ in range(distance):
            head = move_head(direction, distance, head)
            tail = move_tail(head, tail)
            tail_positions.append(tail)
    return len(set(tail_positions))
    
        
def move_head(direction: str, distance: int, head: Position) -> Position:
    match direction:
        case "R":
            head = Position(x=head.x + 1, y=head.y)
        case "L":
            head = Position(x=head.x - 1, y=head.y)
        case "U":
            head = Position(x=head.x, y=head.y + 1)
        case "D":
            head = Position(x=head.x, y=head.y - 1)
    return head


def move_tail(head: Position, tail: Position) -> Position:
    match head.distance(tail):
        case 2: 
            if tail.is_aligned_with(head):
                return Position.midpoint(head, tail)
        case 3 | 4:
            directions = (head.x - tail.x, head.y - tail.y)
            direction_x, direction_y = map(sign, directions)
            result = Position(x=tail.x+direction_x, y=tail.y+direction_y)
            return result
    return tail

def sign(value: int) -> int:
    if value == 0:
        return 0
    return 1 if value > 0 else -1

def solve_part_two(puzzle: List[Tuple[str, int]]) -> int:
    N_KNOTS = 10
    knots = [Position(0, 0) for _ in range(N_KNOTS)]
    tail_positions = [Position(0, 0)]
    for direction, distance in puzzle:
        for _ in range(distance):
            head, *rest = knots
            head = move_head(direction, distance, head)
            prev_knot = head
            rest = [(prev_knot := move_tail(prev_knot, knot)) for knot in rest] 
            knots = [head, *rest]
            tail_positions.append(knots[-1])
    return len(set(tail_positions))


def move_knots(head: Position, knots: Iterable[Position]) -> List[Position]:
    previous_knot = head
    result = []
    for knot in knots:
        previous_knot = move_tail(previous_knot, knot)
        result.append(previous_knot)
    return result

if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
