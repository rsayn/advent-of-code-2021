from typing import Callable, Counter, Dict, List
from functools import partial


CaveGuide = Dict[str, List[str]]
ValidFunc = Callable[[List[str]], bool]


def navigate(cave: str, guide: CaveGuide, path: List[str], valid_fn: ValidFunc = None) -> List[List[str]]:
    if cave == 'end':
        return [path]
    paths = []
    for destination in guide[cave]:
        # go all possible routes if they are valid
        if destination in guide and valid_fn((newpath := path + [destination])):
            paths += navigate(destination, guide, newpath, valid_fn=valid_fn)
    return paths


def is_valid(path: List[str]) -> bool:
    """
    Checks the path is valid.
    """
    counts = Counter(filter(lambda cave: cave.islower(), path))
    return max(counts.values()) == 1

def is_valid_revisited(path: List[str]) -> bool:
    """
    Checks if the path is valid, allowing revisiting ONE small cave.
    """
    counts = Counter(filter(lambda cave: cave.islower(), path))
    total = sum(counts.values())
    return total <= len(counts) + 1 and counts.get('start', 0) < 2 and counts.get('end', 0) < 2

def run(input_path: str, exp_count: int, exp_revisit_count: int) -> None:
    navigate_part1 = partial(navigate, valid_fn=is_valid)
    guide = read_input(input_path)
    paths = navigate_part1('start', guide, ['start'])
    count = len(paths)
    print(f'There are {count} valid paths in the cave system')
    assert count == exp_count

    navigate_part2 = partial(navigate, valid_fn=is_valid_revisited)
    paths = navigate_part2('start', guide, ['start'])
    count = len(paths)
    print(f'There are {count} valid paths in the cave system with revisiting')
    assert count == exp_revisit_count

def read_input(input_path: str) -> CaveGuide:
    with open(f'day12/{input_path}', 'r') as inputfile:
        caves = {}
        for line in inputfile.readlines():
            cave_1, cave_2 = line.strip('\n').split('-')
            caves[cave_1] = caves.get(cave_1, []) + [cave_2]
            caves[cave_2] = caves.get(cave_2, []) + [cave_1]
        caves['end'] = []
    return caves
        
if __name__ == '__main__':
    run('sample_input.txt', 10, 36)
    run('input.txt', 4885, 117095)
