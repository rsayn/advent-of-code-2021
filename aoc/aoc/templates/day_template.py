from typing import *
from pathlib import Path


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


def parse_puzzle_lines(lines: Iterable[str]) -> Any:
    ...


def solve_part_one(puzzle: Any) -> int:
    ...


def solve_part_two(puzzle: Any) -> int:
    ...


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    # run_puzzle("input.txt")
