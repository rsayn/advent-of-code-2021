import dataclasses
import numpy as np
import itertools as it
from typing import *


Index2D = Tuple[int, int]


@dataclasses.dataclass
class OctopusSimulator:
    
    data: np.ndarray
    
    def simulate(self, steps: int) -> int:
        data = self.data.copy()
        total_flash_count = 0
        first_simultaneous_step = -1
        for step in range(steps):
            data, step_flash_count = self.step(data)
            total_flash_count += step_flash_count
            if data.sum() == 0 and first_simultaneous_step == -1:
                first_simultaneous_step = step + 1
        return total_flash_count, first_simultaneous_step
    
    def step(self, data: np.ndarray) -> Tuple[np.ndarray, int]:
        # Increment energy
        data += 1
        flash_index = self.find_energy_over_9(data)
        past_flash_index = []
        while len(flash_index) > 0:
            # Find indices to increment
            neighbours = self.find_all_neighbours(flash_index)
            data = put(data, neighbours, lambda val: val + 1)
            past_flash_index += flash_index
            flash_index = self.remove_existing(self.find_energy_over_9(data), past_flash_index)
        data = put(data, past_flash_index, lambda _: 0)
        return data, len(past_flash_index)
    
    def find_energy_over_9(self, data: np.ndarray) -> List[Index2D]:
        return list(map(tuple, np.argwhere(data > 9).tolist()))
    
    def find_all_neighbours(self, index: List[Index2D]) -> List[Index2D]:
        return [n for idx in index for n in self.find_neighbours(idx)]

    def find_neighbours(self, index: Index2D) -> List[Index2D]:
        row, col = index
        all_neighbours = it.product(range(row-1, row+2), range(col-1, col+2))
        return list(filter(lambda n: n != index and n[0] >= 0 and n[1] >= 0 and n[0] < self.maxsize and n[1] < self.maxsize, all_neighbours))

    def remove_existing(self, arr: List[Any], existing: List[Any]) -> List[Any]:
        return [elem for elem in arr if elem not in existing]

    @property
    def maxsize(self) -> int:
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError('Simulation data is not squared!')
        return self.data.shape[1]

def put(data: np.ndarray, index: List[Index2D], func: Callable[[int], int]) -> np.ndarray:
    for idx in index:
        data[idx] = func(data[idx])
    return data

def run(input_path: str, exp_result: int, exp_first: int, steps: int = 100) -> None:
    matrix = read_input(input_path)
    result, _ = OctopusSimulator(matrix).simulate(steps)
    print(f'In {steps} steps, a total of {result} flash occurred')
    assert result == exp_result

    _, first_simultaneous = OctopusSimulator(matrix).simulate(3000)
    print(f'The first simultaneous step is {first_simultaneous}')
    assert first_simultaneous == exp_first


def read_input(input_path: str) -> np.ndarray:
    with open(f'day11/{input_path}', 'r') as inputfile:
        lines = map(lambda line: list(line.rstrip('\n')), inputfile.readlines())
        return np.array([list(map(int, line)) for line in lines])

if __name__ == '__main__':
    run('sample_input.txt', 1656, 195, steps=100)
    run('input.txt', 1613, 510, steps=100)


