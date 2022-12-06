from collections import deque
from typing import *
from pathlib import Path


ElemT = TypeVar("ElemT")

def solve_part_one(buffer: str) -> int:
    return find_start_of_packet(buffer)

def solve_part_two(buffer: str) -> int:
    return find_start_of_message(buffer)

def find_start_of_packet(buffer: str):
    return find_first_unique_sequence_in_buffer(buffer, 4)
    
def find_start_of_message(buffer: str):
    return find_first_unique_sequence_in_buffer(buffer, 14)

def find_first_unique_sequence_in_buffer(buffer: str, sequence_length: int) -> int:
    windows = windowed(buffer, sequence_length)
    marker = first(windows, lambda window: len(set(window)) == sequence_length)
    return buffer.index("".join(marker)) + len(marker)

def first(iterable: Iterable[ElemT], condition: Callable[[ElemT], bool]) -> ElemT:
    return next(element for element in iterable if condition(element))

def windowed(iterable: Iterable[ElemT], window_size: int) -> Iterator[Tuple[ElemT, ...]]:
    queue = deque()
    for item in iterable:
        queue.append(item)
        if len(queue) == window_size:
            yield tuple(queue)
            queue.popleft()


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


def parse_puzzle_lines(lines: Iterable[str]) -> str:
    return next(iter(lines))




if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
