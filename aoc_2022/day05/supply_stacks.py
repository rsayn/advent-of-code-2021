from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import re
from typing import *
from pathlib import Path
from collections import deque


@dataclass
class CraneMover:
    crane_towers: List[deque]
    instructions: List[Instruction]
    model_code: Literal['9000', '9001'] = "9000"

    def play(self):
        for instruction in self.instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction: Instruction):
        tower_from = self.crane_towers[instruction.move_from-1]
        tower_to = self.crane_towers[instruction.move_to-1]
        self.move_cranes(tower_from, tower_to, instruction.num_blocks)

    def move_cranes(self, tower_from: deque, tower_to: deque, num_cranes: int):
        if self.model_code == "9000":
            for _ in range(num_cranes):
                tower_to.append(tower_from.pop())
        elif self.model_code == "9001":
            cranes = [tower_from.pop() for _ in range(num_cranes)]
            for crane in reversed(cranes):
                tower_to.append(crane)

    def peek(self) -> str:
        return "".join(tower[-1] if len(tower) else "" for tower in self.crane_towers)

    def __repr__(self) -> str:
        return "\n".join(
            f"{i} -> {tower}"
            for i, tower in enumerate(self.crane_towers)
        )

    def with_model_code(self, model_code: Literal["9000", "9001"]) -> CraneMover:
        return CraneMover(
            model_code=model_code,
            crane_towers=deepcopy(self.crane_towers),
            instructions=self.instructions,
        )


@dataclass
class Instruction:
    num_blocks: int
    move_from: int
    move_to: int


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
        yield from (line for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str]) -> CraneMover:
    iterator = iter(lines)
    crates = parse_crate_positions(iterator)
    instructions = parse_instructions(iterator)
    return CraneMover(crates, instructions)


def parse_crate_positions(lines: Iterator[str]) -> List[deque[str]]:
    crate_lines = list(filterwhile(lines, lambda line: bool(line.strip())))
    crate_numbers = [elem for elem in crate_lines[-1].strip().split(" ") if elem]
    crate_indexes = [crate_lines[-1].index(number) for number in crate_numbers]
    crate_towers = [
        deque(reversed([line[index] for line in crate_lines[:-1] if line[index].strip()]))
        for index in crate_indexes
    ]

    return crate_towers


def filterwhile(iterable: Iterable, condition: Callable) -> Iterator:
    iterator = iterable if isinstance(iterable, Iterator) else iter(iterable)
    while (condition(item := next(iterator))):
        yield item


def parse_instructions(lines: Iterator[str]) -> List[Instruction]:
    return [parse_instruction(line) for line in lines]


def parse_instruction(line: str) -> Instruction:
    elements = re.findall(r"^move (\d+) from (\d+) to (\d+)$", line)[0]
    return Instruction(*map(int, elements))


def solve_part_one(puzzle: CraneMover) -> str:
    puzzle = puzzle.with_model_code('9000')
    puzzle.play()
    return puzzle.peek()


def solve_part_two(puzzle: CraneMover) -> str:
    puzzle = puzzle.with_model_code('9001')
    puzzle.play()
    return puzzle.peek()


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
