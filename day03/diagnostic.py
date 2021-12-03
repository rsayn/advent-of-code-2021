from typing import List, Tuple
import numpy as np
from numpy.core.fromnumeric import argmax


def multiply_binary(a: str , b: str):
    """
    Multiplies `a` and `b`, converting them from binary strings.
    """
    return int(a, 2) * int(b, 2)


def find_gamma_and_epsilon(bitlist: List[str]) -> Tuple[str, str]:
    """
    Computes most and least frequent bits for each position in `bitlist`.
    """
    bit_ints = numpy_from_bitlist(bitlist)
    gam, eps = [], []
    for col in range(bit_ints.shape[-1]):
        _, counts = np.unique(bit_ints[:, col], return_counts=True,)
        eps.append(str(np.argmin(counts)))
        gam.append(str(np.argmax(counts)))
    return ''.join(gam), ''.join(eps)


def find_ogr_and_co2_sr(bitlist: List[str]) -> Tuple[str, str]:
    """
    Computes Oxygen Generator Rating and CO2 Scrubber Rating.
    """
    bit_ints = numpy_from_bitlist(bitlist)
    org_bits = bit_ints
    co2_bits = bit_ints.copy()
    for col in range(bit_ints.shape[-1]):
        if org_bits.shape[0] > 1:
            org_bits = org_bits[np.where(org_bits[:, col] == find_bit_by_frequency(org_bits, col, argmax=True))]
        if co2_bits.shape[0] > 1:
            co2_bits = co2_bits[np.where(co2_bits[:, col] == find_bit_by_frequency(co2_bits, col, argmax=False, default=0))]
    if org_bits.shape[0] > 1 or co2_bits.shape[0] > 1:
        raise ValueError('Invalid input')
    return ''.join(org_bits[0].astype(str)), ''.join(co2_bits[0].astype(str))


def find_bit_by_frequency(array: np.ndarray, col: int, argmax: bool = True, default: int = 1) -> int:
    """
    Finds the most (or least) frequent bit in `array` at column `col`.
    If counts are the same, returns `default`.
    """
    unique, counts = np.unique(array[:, col], return_counts=True)
    if counts.shape == (1,):
        return unique[0]
    if counts[0] == counts[1]:
        return default
    if argmax:
        return np.argmax(counts)
    else:
        return np.argmin(counts)


def numpy_from_bitlist(bitlist: List[str]):
    return np.array(list(map(lambda bit: [int(b) for b in list(bit)], bitlist)))

def read_input() -> List[str]:
    with open('day03/input.txt', 'r') as inputfile:
        return inputfile.read().splitlines()


if __name__ == '__main__':
    sample_input = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010',]
    actual_input = read_input()
    
    assert multiply_binary(*find_gamma_and_epsilon(sample_input)) == 198
    assert multiply_binary(*find_gamma_and_epsilon(actual_input)) == 749376

    assert multiply_binary(*find_ogr_and_co2_sr(sample_input)) == 230
    assert multiply_binary(*find_ogr_and_co2_sr(actual_input)) == 2372923


