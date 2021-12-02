import math
import sys
import itertools as it

from typing import Any, Generator, Iterable, List, Literal, Tuple, TypeVar


T = TypeVar('T', bound=Any)


def consecutive_groups(iterable: Iterable[T], size: int = 2) -> Generator[Tuple[T, ...], None, None]:
    """
    Returns an iterator over consecutive pairs in `iterable`.
    """
    elements = []
    for item in iterable:
        elements.append(item)
        if len(elements) == size:
            yield tuple(elements)
            elements = elements[1:]


def consecutive_windows(iterable: Iterable[T], size: int = 2) -> Generator[Tuple[Tuple[T, ...], Tuple[T, ...]], None, None]:
    """
    Returns an iterator over consecutive windows of elements in `iterable`.
    """
    windows_1, windows_2 = it.tee(consecutive_groups(iterable, size=size), 2)
    windows_2 = it.islice(windows_2, 1, sys.maxsize)
    for w1, w2 in zip(windows_1, windows_2):
        yield w1, w2


def compare_measurements(prev: int, next: int) -> Literal[-1, 0, 1]:
    """
    Compares two ints.

    Returns:
      -1 if prev >  next
      0  if prev == next
      +1 if prev <  next
    """
    if prev == next:
        return 0
    return int(math.copysign(1, next-prev))


def compare_windows(w1: Tuple[int, ...], w2: Tuple[int, ...]) -> Literal[-1, 0, 1]:
    """
    Compares measurements as a sum of rolling windows.
    """
    return compare_measurements(sum(w1), sum(w2))


def count_increases(measurements: List[int], rolling: int = 1) -> int:
    """
    Counts the number of times where a value in `measurements` is larger than the previous.
    """
    if rolling == 1:
        return sum(filter(lambda val: val > 0, it.starmap(compare_measurements, consecutive_groups(measurements))))
    else:
        return sum(filter(lambda val: val > 0, it.starmap(compare_windows, consecutive_windows(measurements, size=rolling))))


def read_input() -> List[int]:
    with open('day1/input.txt', 'r') as inputfile:
        return list(map(int, inputfile.readlines()))

if __name__ == '__main__':
    sample_measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    actual_measurements = read_input()
    assert count_increases(sample_measurements) == 7
    assert count_increases(actual_measurements) == 1832

    assert count_increases(sample_measurements, rolling=3) == 5
    assert count_increases(actual_measurements, rolling=3) == 1858
