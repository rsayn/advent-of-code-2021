from typing import Any, List, Tuple
import numpy as np
import dataclasses
import itertools as it


Index2D = List[Tuple[int, int]]


@dataclasses.dataclass
class SmokeBasin:
    """
    Avoid the lava tubes!
    """

    heightmap: np.ndarray
    """
    Matrix of height values in the cave.
    """
    
    def find_low_points(self) -> Index2D:
        """
        Finds low points in the cave using `heightmap`.
        """
        return list(filter(self.is_low_point, it.product(range(self.maxrow), range(self.maxcol))))

    def find_basins(self) -> List[List[Tuple[int, int]]]:
        """
        Creates a basin from each low point.
        """
        return list(map(self.expand_basin, self.find_low_points()))
    
    def expand_basin(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Recursively expands basin from `point`, looking for neighbors with higher values than the current point.
        """
        basin = []
        if (value := self.heightmap[point]) == 9:
            return basin
        for neighbor in filter(lambda neigh: self.heightmap[neigh] > value, self.neighbors(*point)):
            basin += self.expand_basin(neighbor)
        return list(set([point] + basin))

    def is_low_point(self, point: Tuple[int, int]) -> bool:
        values = [(value := self.heightmap[point])] + arrayget(self.heightmap, self.neighbors(point))
        return 0 == np.argmin(values) and value != np.mean(values)

    def neighbors(self, point: Tuple[int, int]) -> Index2D:
        """
        Returns neighbor indices of the node in position `[row, col]`.
        """
        row, col = point
        left = col - 1 if col > 0 else None
        right = col + 1 if col + 1 < self.maxcol else None
        up = row - 1 if row > 0 else None
        down = row + 1 if row + 1 < self.maxrow else None
        return list(filter(lambda sublist: None not in sublist, [(row, left), (row, right), (up, col), (down, col)]))

    @property
    def maxrow(self) -> int:
        return self.heightmap.shape[0]
    
    @property
    def maxcol(self) -> int:
        return self.heightmap.shape[1]

def arrayget(arr: np.ndarray, index: Index2D) -> List[Any]:
    return [arr[idx] for idx in index]

def compute_risk_level(low_points: List[int]) -> int:
    return sum(low_points) + len(low_points)

def compute_total_basin_value(basins: List[List[Tuple[int, int]]]) -> int:
    one, two, three = sorted(list(map(len, basins)), reverse=True)[:3]
    print(f'Sizes: {one}, {two}, {three}')
    return one * two * three

def read_input(input_path: str) -> SmokeBasin:
    with open(f'day09/{input_path}', 'r') as inputfile:
        heightmap = np.array([list(map(int, list(line.replace('*', '').strip('\n')))) for line in inputfile.readlines()])
        return SmokeBasin(heightmap=heightmap)


def run(input_path: str, exp_count: int, exp_total: int, exp_basin_value: int) -> None:
    smoke_basin = read_input(input_path)
    print(smoke_basin.heightmap.shape)
    low_points = smoke_basin.find_low_points()
    total_risk_level = compute_risk_level(arrayget(smoke_basin.heightmap, low_points))
    print(f'There are {len(low_points)} low points in the cave; the sum of the risk levels is {total_risk_level}')
    assert len(low_points) == exp_count
    assert total_risk_level == exp_total

    basins = smoke_basin.find_basins()
    total_basin_value = compute_total_basin_value(basins)
    print(f'There are {len(basins)} basins in the cave; the product of the three largest basins is {total_basin_value}')
    assert len(basins) == exp_count
    assert total_basin_value == exp_basin_value



if __name__ == '__main__':
    run('sample_input.txt', 4, 15, 1134)
    run('input.txt', 247, 600, 987840)
