
from pathlib import Path
from typing import List


Calories = List[int]

FOLDER = Path(__file__).parent


def read_input(input_file: str) -> List[Calories]:
    with open(FOLDER / input_file, 'r') as inputfile:
        lines = inputfile.readlines()
        return parse_elves_calories(lines)


def parse_elves_calories(lines: List[str]) -> List[Calories]:
    elves = []
    calories = []
    for line in (line.strip() for line in lines):
        if not line:
            elves.append(calories)
            calories = []
        else:
            calories.append(int(line))
    return elves


def find_most_caloric_elves(elves_calories: List[Calories], limit: int = 1) -> int:
    total_calories = (sum(calories) for calories in elves_calories)
    return sum(sorted(list(total_calories), reverse=True)[:limit])


def run_puzzle(file: str):
    calories = read_input(file)
    most_calories = find_most_caloric_elves(calories)
    print(f"The elf with most calories on {file} is carrying {most_calories}")

    top3_most_calories = find_most_caloric_elves(calories, limit=3)
    print(f"The top 3 calory-carrying elves are carrying {top3_most_calories} in total")


if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
    

