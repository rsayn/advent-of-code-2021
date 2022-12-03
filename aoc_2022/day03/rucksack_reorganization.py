from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from itertools import chain
import string
from typing import *
from pathlib import Path


@dataclass
class Rucksack:
    left_compartment: Compartment
    right_compartment: Compartment

    def find_wrong_items(self) -> List[str]:
        return list(self.left_compartment.intersection(self.right_compartment))

    def all_items(self) -> List[str]:
        return self.left_compartment.items + self.right_compartment.items
    
    def unique_items(self) -> Set[str]:
        return set(self.all_items())


@dataclass
class Compartment:
    items: List[str]

    def unique_items(self) -> Set[str]:
        return set(self.items)
    
    def intersection(self, other: Compartment) -> Set[str]:
        return self.unique_items().intersection(other.unique_items())


def run_puzzle(filename: str):
    """
    Runs today's puzzle.
    """
    FOLDER = Path(__file__).parent
    puzzle_lines = read_puzzle_lines(FOLDER / filename)
    puzzle_content = parse_puzzle_lines(puzzle_lines)
    result_one = compute_part_one(puzzle_content)
    print(f"The result for part 1 is {result_one}")
    result_two = compute_part_two(puzzle_content)
    print(f"The result for part 2 is {result_two}")


def read_puzzle_lines(filepath: Path) -> Iterator[str]:
    """
    Reads the AOC puzzle input.
    """
    with open(filepath, "r") as puzzle_file:
        yield from (line.strip() for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str]) -> List[Rucksack]:
    split_lines = (split_compartments(line) for line in lines)
    return [Rucksack(left, right) for left, right in split_lines]


def split_compartments(line: str) -> Tuple[Compartment, Compartment]:
    split_point = int(len(line) / 2)
    left, right = list(line[:split_point]), list(line[split_point:])
    return Compartment(left), Compartment(right)


def compute_part_one(rucksacks: List[Rucksack]) -> int:
    wrong_items = list(chain(*(rucksack.find_wrong_items() for rucksack in rucksacks)))
    priorities = list(map(item_to_priority, wrong_items))
    total_priority = sum(priorities)
    return total_priority

PRIORITIES = {
    letter: index for index, letter in enumerate(chain(string.ascii_letters), start=1)
}

def item_to_priority(item: str) -> int:
    return PRIORITIES[item]


def compute_part_two(rucksacks: List[Rucksack]) -> int:
    elf_groups = grouped(rucksacks, groupsize=3)
    badges = (find_bagde(elf_group) for elf_group in elf_groups)
    priorities = map(item_to_priority, badges)
    return sum(priorities)


ElemT = TypeVar("ElemT")

def grouped(iterable: Iterable[ElemT], groupsize: int = 2) -> Iterable[Tuple[ElemT, ...]]:
    group = []
    for element in iterable:
        group.append(element)
        if len(group) == groupsize:
            yield tuple(group)
            group = []
    if len(group):
        yield tuple(group)


def find_bagde(group: Tuple[Rucksack, ...]) -> str:
    shared_items = reduce(set.intersection, (rucksack.unique_items() for rucksack in group))
    return list(shared_items)[0]


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
