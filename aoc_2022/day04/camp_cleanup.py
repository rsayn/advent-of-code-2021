from __future__ import annotations
from dataclasses import dataclass
from typing import *
from pathlib import Path


@dataclass
class Assignment:
    start: int
    end: int

    def __contains__(self, other: Any) -> bool:
        interval = range(self.start, self.end+1)
        if isinstance(other, int):
            return other in interval
        if isinstance(other, Assignment):
            return (other.start in interval and other.end in interval)
        return NotImplemented

    def overlaps_with(self, other: Assignment) -> bool:
        return any(right.start in left or right.end in left for left, right in [(self, other), (other, self)])


def run_puzzle(filename: str):
    """
    Runs today's puzzle.
    """
    FOLDER = Path(__file__).parent
    puzzle_lines = read_puzzle_lines(FOLDER / filename)
    puzzle_content = parse_puzzle_lines(puzzle_lines)
    result_one = compute_part_1(puzzle_content)
    print(f"The result for part 1 is {result_one}")
    result_two = compute_part_2(puzzle_content)
    print(f"The result for part 2 is {result_two}")


def read_puzzle_lines(filepath: Path) -> Iterator[str]:
    """
    Reads the AOC puzzle input.
    """
    with open(filepath, "r") as puzzle_file:
        yield from (line.strip() for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str]) -> List[Tuple[Assignment, Assignment]]:
    return [
        (assignment_from_section(first_section), assignment_from_section(second_section))
        for first_section, second_section in (line.split(",") for line in lines)
    ]

def assignment_from_section(section: str) -> Assignment:
    section_range = map(int, section.split("-"))
    return Assignment(*section_range)


def compute_part_1(assignment_pairs: List[Tuple[Assignment, Assignment]]) -> int:
    return count_pairs(assignment_pairs, lambda left, right: left in right or right in left)


def compute_part_2(assignment_pairs: List[Tuple[Assignment, Assignment]]) -> int:
    return count_pairs(assignment_pairs, lambda left, right: left.overlaps_with(right))


def count_pairs(pairs, condition) -> int:
    return sum(1 for left, right in pairs if condition(left, right))


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")

    a1 = Assignment(5, 9)
    a2 = Assignment(4, 10)
    print(a1.overlaps_with(a2))
