
from typing import Counter, List


def lanternfish_simulation(initial_fish_timers: List[int], days: int = 80) -> None:
    """
    Performs a lantern fish spawning simulation up to `days` from now. 
    """
    lanternfish_timers = Counter(initial_fish_timers)
    lanternfish_timers[7] = 0
    lanternfish_timers[8] = 0
    round_newborns = 0
    for _ in range(days):
        round_newborns = lanternfish_timers[0]
        for day in range(len(lanternfish_timers)):
            lanternfish_timers[day] = lanternfish_timers[day+1] if day < 8 else round_newborns
        lanternfish_timers[6] += round_newborns
    return sum(lanternfish_timers.values())


def read_input(input_path: str) -> List[int]:
    with open(f'day06/{input_path}', 'r') as inputfile:
        return list(map(int, inputfile.read().split(',')))


def run(input_path: str, expected_count: int, days: int) -> None:
    fish_timers = read_input(input_path)
    count = lanternfish_simulation(fish_timers, days=days)
    print(f'After {days} days, there are {count} fish')
    assert count == expected_count


if __name__ == '__main__':
    # Part I
    run('sample_input.txt', 5934, 80)
    run('input.txt', 352195, 80)

    # Part II
    run('sample_input.txt', 26984457539, 256)
    run('input.txt', 1600306001288, 256) 
