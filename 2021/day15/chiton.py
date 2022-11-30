import itertools
import numpy as np
import networkx as nx
from functools import cache

from typing import *


Point = Tuple[int, int]


def dijkstra(G: nx.Graph, source: Point, target: Point, weight: str = 'w') -> List[Point]:
    costs = {node: np.inf for node in G.nodes}
    Q = list(G.nodes)
    costs[source] = 0
    path = {}
    visited = set()

    while len(Q) > 0:
        node = min(Q, key=costs.get)
        visited.add(node)
        Q.remove(node)
        if costs[node] == np.inf:
            break
        if node == target:
            return build_path(path, source, target)
        for neighbor in G[node]:
            cost = costs[node] + G[node][neighbor][weight]
            if neighbor not in visited:
                if cost < costs[neighbor]:
                    costs[neighbor] = cost
                    path[neighbor] = node
    return []

def build_path(prec: Dict[Point, Point], source: Point, target: Point):
    path = [target]
    point = target
    while point != source:
        path.append(prec[point])
        point = prec[point]
    return list(reversed(path))

def run(input_path: str, exp_result_1: int, exp_result_2: int) -> None:
    matrix = read_matrix(input_path)
    G, target = build_graph(matrix)
    path = dijkstra(G, (0,0), target)
    cost = compute_cost(matrix, path)
    # print(path_weight(G, path, weight='w'))
    print(f'The path with the minimum cost has len {len(path)} and a cost of {cost}')
    assert cost == exp_result_1

    bigger_matrix = build_matrix(matrix)
    bigger_graph, target  = build_graph(bigger_matrix)
    path = dijkstra(bigger_graph, (0,0), target, weight='w')
    cost = compute_cost(bigger_matrix, path)
    print(f'The path with the minimum cost has len {len(path)} and a cost of {cost}')
    assert cost == exp_result_2

def build_matrix_for(matrix: np.ndarray, num: int) -> np.ndarray:
    mtx = matrix + num
    mtx[mtx > 9] = mtx[mtx > 9] % 9
    return mtx

def build_matrix(matrix: np.ndarray) -> np.ndarray:
    rows = []
    for numrow in range(5):
        row = []
        for numcol in range(5):
            row.append(build_matrix_for(matrix, numrow + numcol))
        rows.append(np.concatenate(row, axis=1))
    return np.array(np.concatenate(rows, axis=0))

def build_graph(matrix: np.ndarray) -> Tuple[nx.Graph, Point]:
    maxrow, maxcol = matrix.shape
    G = nx.DiGraph()
    points = list(itertools.product(range(0, maxrow), range(0, maxcol)))
    G.add_nodes_from(points)
    for point in points:
        for neigh in neighbors(point, maxrow, maxcol):
            cost = matrix[neigh[0]][neigh[1]]
            G.add_edge(point, neigh, w=cost)
    return G, (maxrow-1, maxcol-1)

def compute_cost(matrix, path) -> int:
    return sum(matrix[point] for point in path) - matrix[0, 0]

def read_matrix(input_path: str) -> np.ndarray:
    with open(f'day15/{input_path}', 'r') as inputfile:
        return np.array([[int(elem) for elem in line.strip()] for line in inputfile.readlines()])

@cache
def neighbors(point: Tuple[int, int], maxrow: int, maxcol: int) -> Point:
    """
    Returns neighbor indices of the node in position `[row, col]`.
    """
    row, col = point
    left = col - 1 if col > 0 else None
    right = col + 1 if col + 1 < maxcol else None
    up = row - 1 if row > 0 else None
    down = row + 1 if row + 1 < maxrow else None
    return list(filter(lambda sublist: None not in sublist, [(row, left), (row, right), (up, col), (down, col)]))


if __name__ == '__main__':
    run('sample_input.txt', 40, 315)
    run('input.txt', 714, -1)
