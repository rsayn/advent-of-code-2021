

import numpy as np
from typing import Iterator, List, Tuple
from functools import lru_cache


def compute_best_crab_position_1(positions: List[int]) -> Tuple[int, int]:
    """
    Finds the best spot to accumulate all crabs with minimal fuel expense.

    Turns out the computation is slightly more complicated though...
    """
    pos_array = np.array(positions)
    return (pos := np.median(pos_array).astype(int)), np.sum(np.abs(pos_array - pos))


def compute_best_crab_position_2(positions: List[int]) -> Tuple[int, int]:
    """
    Finds the best spot to accumulate all crabs with minimal fuel expense.

    This time taking into account the laws of crab engineering...
    """
    pos_array = np.array(sorted(positions))
    best_pos, best_fuel = -1, np.inf

    for pos in iterpos(pos_array):
        if (fuel := np.sum(list(map(movement_cost, np.abs(pos_array - pos))))) < best_fuel:
            best_fuel = fuel
            best_pos = pos
    return best_pos, best_fuel


def iterpos(positions: np.ndarray) -> Iterator[int]:
    """
    Optimized iterator over `positions`.

    Tries reducing complexity by removing extreme values (if it's worth it).
    """
    if len(positions) < 100:
        minval, maxval = positions.min(), positions.max() + 1
    else:
        minval, maxval = np.percentile(positions, 25).astype(int), np.percentile(positions, 75).astype(int)
    return iter(range(minval, maxval))


OPT_VALUE = 30
"""
Optimization value to maximize cache hits on `movement_cost` function.
"""


@lru_cache()
def movement_cost(move_size: int) -> int:
    """
    Movement cost calculation when taking into account crab engineering.

    Calculation is split into parts to make use of the cache.
    """
    remainder, times = move_size % OPT_VALUE, move_size // OPT_VALUE
    if remainder == 0 or times == 0:
        return int(move_size * (move_size / 2) + (move_size / 2))
    return (movement_cost(base := (times * OPT_VALUE))) + (base * remainder + movement_cost(remainder))


def read_input(input_path: str) -> List[int]:
    with open(f'day07/{input_path}', 'r') as file:
        return list(map(int, file.read().split(',')))


def run(input_path: str, exp_pos: int, exp_fuel: int, part: int = 1) -> None:
    positions = read_input(input_path)
    if part == 1:
        pos, fuel = compute_best_crab_position_1(positions)
    else:
        pos, fuel = compute_best_crab_position_2(positions)
    print(f'The best crab alignment spot is {pos} with {fuel} fuel units spent')
    assert (pos, fuel) == (exp_pos, exp_fuel)


if __name__ == '__main__':
    # Part I
    run('sample_input.txt', 2, 37, part=1)
    run('input.txt', 345, 348996, part=1)

    # # Part II
    run('sample_input.txt', 5, 168, part=2)
    run('input.txt', 481, 98231647, part=2)
