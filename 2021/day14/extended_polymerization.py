
import os
import sys
sys.path.append(os.path.abspath('.'))

from typing import *
from functools import reduce

from day01.submarine import consecutive_groups

def run_steps(template: str, rules: Dict[str, str], steps: int) -> str:
    return reduce(lambda acc, _: step(acc, rules), range(steps), template)

def step(template: str, rules: Dict[str, str]) -> str:
    resulting_template = template
    for i, pair in enumerate(map(''.join, consecutive_groups(template, size=2))):
        split_index = i * 2 + 1
        before, after = resulting_template[:split_index], resulting_template[split_index:]
        resulting_template = f'{before}{rules.get(pair, "")}{after}'
    return resulting_template

def run_steps_only_count(template: str, rules: Dict[str, str], steps: int) -> Dict[str, int]:
    counts = Counter(list(map(''.join, consecutive_groups(template, size=2))))
    for _ in range(steps):
        counts = step_with_counts(counts, rules)
    return counts

def step_with_counts(counts: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    next_counts = counts.copy()
    for pair, occurrences in counts.items():
        if pair not in rules:
            continue
        pair1, pair2 = pair[0] + rules[pair], rules[pair] + pair[1]
        next_counts[pair] -= occurrences
        next_counts[pair1] = next_counts.get(pair1, 0) + occurrences
        next_counts[pair2] = next_counts.get(pair2, 0) + occurrences
    return next_counts


def count_occurrences(result: str) -> Dict[str, int]:
    counts = Counter(result)
    return counts.most_common(1)[0][1], counts.most_common()[-1][1]

def count_letters(template: str, pair_counts: Dict[str, int]) -> Dict[str, int]:
    letter_counts = {}
    for (_, second_letter), occurrences in pair_counts.items():
        letter_counts[second_letter] = letter_counts.get(second_letter, 0) + occurrences
    letter_counts[template[0]] += 1
    return letter_counts


def run(input_path: str, exp_result_1: int, exp_result_2: int) -> None:
    polymer, rules = read_input(input_path)
    resulting_polymer = run_steps(polymer, rules, 10)
    most_freq, least_freq = count_occurrences(resulting_polymer)
    result = most_freq - least_freq
    print(f'After 10 steps, occurrences from most_frequent - least_frequent is {result}')
    assert result == exp_result_1

    pair_counts = run_steps_only_count(polymer, rules, 40)
    counts = count_letters(polymer, pair_counts)
    most_freq = max(counts.values())
    least_freq = min(counts.values())
    result = most_freq - least_freq
    print(f'After 40 steps, occurrences from most_frequent - least_frequent is {result}')
    assert result == exp_result_2

def read_input(input_path: str) -> Tuple[str, Dict[str, str]]:
    with open(f'day14/{input_path}', 'r') as inputfile:
        lines = inputfile.readlines()
    return lines[0].strip(), dict(map(lambda line: tuple(line.strip().split(' -> ')), lines[2:]))

if __name__ == '__main__':
    run('sample_input.txt', 1588, 2188189693529)
    run('input.txt', 2170, 2422444761283)
