import dataclasses
import numpy as np
from typing import *
from functools import reduce


Point = NamedTuple('Point', [('x', int), ('y', int)])
FoldDirection = Literal['horizontal', 'vertical']


@dataclasses.dataclass
class Paper:
    """
    A sheet of paper.

    Oftentimes, scissors is a better choice...
    """
    coords: np.ndarray
    """
    Matrix of marked/markable locations on the sheet.
    """
    transparent: bool = True
    """
    Whether this piece of paper is transparent or not
    """

    def mark_locations(self, locations: List[Point]) -> None:
        self.coords = put(self.coords,  locations, lambda _: 1)
    
    def fold(self, along: int, direction: FoldDirection) -> None:
        axis = 0 if direction == 'vertical' else 1
        a = np.take(self.coords, range(0, along), axis=axis)
        b = self.flip(np.take(self.coords, range(along+1, self.coords.shape[axis]), axis=axis), direction)
        self.coords = a + b

    def flip(self, matrix: np.ndarray, direction: FoldDirection) -> np.ndarray:
        flipped = np.array(list(reversed(matrix if direction == 'vertical' else matrix.T)))
        return flipped if direction == 'vertical' else flipped.T

    @property
    def marked_locations(self) -> List[Point]:
        return list(map(lambda o: Point(*o), np.argwhere(self.coords > 0).tolist()))
    
    def __repr__(self) -> str:
        return '\n'.join([''.join(['.' if val == 0 else '#' for val in row]) for row in self.coords])

    @classmethod
    def from_points(cls, points: List[Point]) -> "Paper":
        max_x = max(map(lambda p: p.x, points)) + 1
        max_y = max(map(lambda p: p.y, points)) + 1
        paper = Paper(coords=np.zeros((max_x, max_y), dtype=np.int8), transparent=True)
        paper.mark_locations(points)
        return paper


def put(data: np.ndarray, index: List[Point], func: Callable[[int], int]) -> np.ndarray:
    for idx in index:
        data[idx] = func(data[idx])
    return data


def read_input(input_path: str) -> Tuple[List[Point], List[Tuple[FoldDirection, int]]]:
    with open(f'day13/{input_path}', 'r') as inputfile:
        lines = inputfile.readlines()
        point_lines = map(lambda l: l.split(','), filter(lambda l: l.strip() and not l.startswith('fold'), lines))
        instr_lines = filter(lambda l: l.startswith('fold'), lines)
        points = list(map(lambda point: Point(int(point[1]), int(point[0])), point_lines))
        instructions = map(lambda l: tuple(l.strip('\n').split(' ')[-1].split('=')), instr_lines)
        instructions = list(map(lambda instr: ('horizontal' if instr[0] == 'x' else 'vertical', int(instr[1])), instructions))
    return points, instructions


def run(input_path: str, exp_count_first: int, exp_count: int) -> None:
    points, instructions = read_input(input_path)
    paper = Paper.from_points(points)
    count_after_first = None
    for direction, along in instructions:
        paper.fold(along, direction)
        if count_after_first is None:
            count_after_first = len(paper.marked_locations)
            print(f'After the first fold, there are {count_after_first} marked dots')
            assert count_after_first == exp_count_first
    
    count = len(paper.marked_locations)
    print(f'After all folds, there are {count} marked dots')
    print('\n' + '-' * paper.coords.shape[1])
    print(repr(paper))
    print('-' * paper.coords.shape[1] + '\n')
    assert count == exp_count


if __name__ == '__main__':
    run('sample_input.txt', 17, 16)
    run('input.txt', 807, 98)
