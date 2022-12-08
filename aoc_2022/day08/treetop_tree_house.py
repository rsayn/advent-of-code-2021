from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from itertools import chain, takewhile
from typing import *
from pathlib import Path


@dataclass
class TreePatch:
    trees: List[List[int]]
    
    def __getitem__(self, key: Any) -> Any:
        return self.trees[key]

    @cached_property
    def T(self) -> TreePatch:
        return TreePatch(trees=transpose(self.trees))

    @property
    def edge_trees(self) -> List[int]:
        return list(chain(self[0], self.T[0][1:-1], self.T[-1][1:-1], self[-1]))

    def __repr__(self) -> str:
        return "\n".join(
            [" ".join(list(map(str, line))) for line in self.trees]
        )


def transpose(iterable: Iterable[Iterable]) -> List[List]:
    return list(zip(*iterable))


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


def parse_puzzle_lines(lines: Iterable[str]) -> TreePatch:
    return TreePatch(trees=[list(map(int, line)) for line in lines])


def solve_part_one(patch: TreePatch) -> int:
    visible = find_visible_trees(patch)
    return len(visible)


def find_visible_trees(patch: TreePatch) -> List[Index]:
    visible_from_left_right = _visible_from_left_right(patch)
    visible_from_top_down = _visible_from_left_right(patch.T)
    indexes = set(visible_from_left_right + [(c, r) for r, c in visible_from_top_down])
    indexes = sorted(list(indexes))
    return indexes

Index = Tuple[int, int]


def _visible_from_left_right(patch: TreePatch) -> List[Index]:
    visible_trees = []
    for index, line in enumerate(patch.trees):
        left_visible = [(index, tree_index) for tree_index in _visible_from_left(line)]
        right_visible = [(index, len(line) -1 - tree_index) for tree_index in _visible_from_left(reversed(line))]
        visible_trees += list(set(left_visible + right_visible))
    return visible_trees


def _visible_from_left(line: Iterable[int]) -> List[int]:
    visible_trees = [0]
    iterator = iter(line)
    highest_tree = next(iterator)
    for index, tree in enumerate(iterator, 1):
        if tree > highest_tree:
            highest_tree = tree
            visible_trees.append(index)
    return visible_trees


def solve_part_two(patch: TreePatch) -> int:
    visible_trees = find_visible_trees(patch)
    return max(scenic_score(tree, patch) for tree in visible_trees)

def scenic_score(tree: Index, patch: TreePatch) -> int:
    score = (
        visible_trees_left_right(tree, patch)
        * visible_trees_left_right(tuple(reversed(tree)), patch.T)
    )
    return score

def visible_trees_left_right(tree: Index, patch: TreePatch) -> int:
    row, col = tree
    line = patch[row]
    height = line[col]
    return (
        count_visible_trees(height, line[col+1:])
        * count_visible_trees(height, reversed(line[0:col]))
    )

def count_visible_trees(height: int, trees: Iterable[int]) -> int:
    trees = list(trees)
    visible = takewhile(lambda tree: tree < height, trees)
    score = len(list(visible))
    return score if score == len(trees) else score + 1


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
