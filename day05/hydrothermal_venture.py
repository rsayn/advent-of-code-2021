


import dataclasses
from functools import reduce
from typing import Counter, Iterable, List, Tuple
from parse import compile


@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass
class VentLine:
    start: Point
    end: Point

    def coverage(self, use_diagonal: bool = False) -> List[Tuple[int, int]]:
        if not use_diagonal:
            if self.start.x != self.end.x and self.start.y != self.end.y:
                return []
        xiter = irange(self.start.x, self.end.x)
        yiter = irange(self.start.y, self.end.y)
        if self.start.x == self.end.x:
            xiter = [self.end.x for _ in range(abs(self.end.y - self.start.y)+1)]
        if self.start.y == self.end.y:
            yiter = [self.end.y for _ in range(abs(self.end.x - self.start.x)+1)]
        return list(map(tuple, zip(xiter, yiter)))


def irange(start: int, stop: int) -> Iterable[int]:
    step = -1 if start > stop else 1
    return range(start, stop+step, step)


def count_overlaps(vent_lines: List[VentLine], threshold: int = 2, use_diagonal: bool = False) -> None:
    """
    Counts overlapping vent line points.
    """
    all_coverage = reduce(lambda acc, vent_line: acc + vent_line.coverage(use_diagonal=use_diagonal), vent_lines, [])
    c = Counter(all_coverage)
    return {k: v for k, v in c.items() if v >= threshold}


def read_input(input_path: str) -> List[VentLine]:
    """
    Parses the input file using `parse`.
    """
    pattern = compile('{x1},{y1} -> {x2},{y2}\n')
    with open(f'day05/{input_path}', 'r') as inputfile:
        result = map(pattern.parse, inputfile.readlines())
        return list(map(lambda r: VentLine(
            start=Point(int(r['x1']), int(r['y1'])), 
            end=Point(int(r['x2']), int(r['y2']))), result))


def run(input_path: str, expected_counts: Tuple[int]) -> None:
    vent_lines = read_input(input_path)
    over2_nodiag = count_overlaps(vent_lines, threshold=2)
    print(f'Found {len(over2_nodiag)} points with at least 2 overlapping lines (no diagonals)')
    assert len(over2_nodiag) == expected_counts[0]

    over2_diag = count_overlaps(vent_lines, threshold=2, use_diagonal=True)
    print(f'Found {len(over2_diag)} points with at least 2 overlapping lines (with diagonals)')
    assert len(over2_diag) == expected_counts[1]

if __name__ == '__main__':
    run('sample_input.txt', (5, 12))
    run('input.txt', (5774, 18423))
