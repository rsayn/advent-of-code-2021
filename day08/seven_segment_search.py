import dataclasses
from typing import Any, Callable, Counter, Dict, Iterable, List, Optional, TypeVar
from itertools import chain


@dataclasses.dataclass
class SevenSegmentData:
    """
    Single data entry for a 7-segment.
    """
    input: List[str]
    output: List[str]

    @classmethod
    def from_line(cls, line: str) -> "SevenSegmentData":
        """
        Reads input and output data from a line of text.
        """
        data = SevenSegmentData(
            input=(parts := line.split('|'))[0].split(),
            output=parts[1].strip('\n').strip().split(),
        )
        assert len(data.input) == 10
        assert len(data.output) == 4
        return data


UNIQUE_DIGITS = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }


def find_unique_digits(data: List[SevenSegmentData]) -> Dict[int, int]:
    """
    Finds the number of unique digits contained in a list of segment data elements.
    """
    counts = Counter(map(len, chain(*(elem.output for elem in data))))
    return { digit: counts[digit_size] for digit, digit_size in UNIQUE_DIGITS.items() }


def find_unique_segments(strings: List[str]) -> Dict[int, str]:
    """
    Finds the corresponding segment string for each of the "easy" digits by checking the output size.
    """
    unique_values = {}
    unique_index = { value: key for key, value in UNIQUE_DIGITS.items() }
    for value in strings:
        if (size := len(value)) in unique_index:
            unique_values[unique_index[size]] = strsort(value)
        if len(unique_values) == 4:
            return unique_values
    raise ValueError('Could not find a suitable value for all unique digits')


def strsort(value: str) -> str:
    """
    Sorts letters in `value` alhabetically.
    """
    return ''.join(sorted(value))

def decode_segment_data(data: List[SevenSegmentData]) -> List[int]:
    """
    Decodes each item in `data`, using its input segments to infer which digit corresponds to each segment string.
    """
    result = []
    for elem in data:
        known_digits = find_unique_segments(elem.input + elem.output)
        strings = list(map(strsort, elem.input + elem.output))
        known_digits[0] = find_match(strings, 8, 6, [4, 1], known_digits)
        known_digits[6] = find_match(strings, 8, 6, [1], known_digits)
        known_digits[5] = find_match(strings, 8, 5, [8, 6], known_digits)
        known_digits[9] = find_match(strings, 8, 6, [8, 5], known_digits, strict=True)
        known_digits[2] = find_match(strings, 8, 5, [4], known_digits, strict=True)
        known_digits[3] = find_match(strings, 8, 5, [0], known_digits, strict=True)
        result.append(segment_output_to_int(elem.output, known_digits))
    return result


def find_match(strings: List[str], base: int, size: int, subs: List[int], known_digits: Dict[int, str], strict: bool = True) -> str:
    """
    Utility function. Same as find + digit_matcher, but returns a sorted version of the string.
    """
    value = find(digit_matcher(base, size, subs, known_digits, strict=strict), strings)
    if value is None:
        raise ValueError('Found None')
    return strsort(value)


def digit_matcher(base: int, size: int, subs: List[int], known_digits: Dict[int, str], strict: bool = True) -> Callable[[str], bool]:
    """
    Creates a matcher function that uses `known_digits` to find a digit using segments in `base`.

    The matcher starts from segments in `base`, builds a set for segments that are assumed to be in
    `base - segments_in_unknown_digit` and then checks the provided input value to see if it matches.
    """
    sub_base = set(known_digits[subs[0]])
    if len(subs) > 1:
        for sub in subs[1:]:
            sub_base = set(sub_base) - set(known_digits[sub])
    digits = (set(known_digits[base]))

    def matcher(value: str) -> bool:
        """
        Checks if `value` matches the lookup criteria for the new digit.
        """
        if len(value) != size or strsort(value) in known_digits.values():
            return False
        if strict:
            return (digits - set(value)).issubset(sub_base)
        else:
            return sub_base.issubset(digits - set(value))
    return matcher



def segment_output_to_int(values: List[str], known_digits: Dict[int, str]) -> int:
    """
    Decodes strings in `values` as ints using `known_digits` as a vocabulary, then concatenates them.
    """
    reverse = { value: key for key, value in known_digits.items() }
    sequence = ''.join(list(map(lambda value: str(reverse[strsort(value)]), values)))
    return int(sequence)


T = TypeVar('T', bound=Any)

def find(func: Callable[[T], bool], iterable: Iterable[T]) -> Optional[T]:
    """
    Finds the first element in `iterable` for which `func` returns `True`, if it exists.
    """
    return next((item for item in iterable if func(item)), None)


def read_input(input_path: str) -> List[SevenSegmentData]:
    with open(f'day08/{input_path}', 'r') as inputfile:
        return list(map(SevenSegmentData.from_line, inputfile.readlines()))


def run(input_path: str, expectected_count: int, exp_result: int) -> None:
    segment_data = read_input(input_path)
    counts = find_unique_digits(segment_data)
    print(f'There are {sum(counts.values())} instances of unique digits')
    assert sum(counts.values()) == expectected_count
    
    result = sum(decode_segment_data(segment_data))
    print(f'Total decoded output is {result}')
    assert result == exp_result


if __name__ == '__main__':
    run('sample_input.txt', 26, 61229)
    run('input.txt', 532, 1011284)
