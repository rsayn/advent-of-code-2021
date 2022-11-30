import dataclasses
from typing import Any, Callable, Iterable, List, Literal, Optional, Tuple, TypeVar, Union

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


Action = Tuple[List[int], str, Union[int, Literal['pop']]]


class ParserException(Exception):
    """
    Exception raised by the parser.
    """
    error_index: int
    error_char: str

    def __init__(self, *args, error_index: int = -1, error_char: str = "Unknown", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.error_index = error_index
        self.error_char = error_char


@dataclasses.dataclass
class ChunkParser:
    actions: List[Action]

    def parse(self, text: str) -> List[int]:
        state = [0]
        for i, char in enumerate(text):
            next_state = self.next_state(state[-1], char)
            if next_state == 'pop':
                state.pop()
            elif next_state == -1:
                raise ValueError(f"Syntax error at char {i}", i, char)
            else:
                state.append(next_state)
        return state
    
    def complete(self, state: List[int]) -> str:
        completion = ''
        for item in reversed(state):
            match item:
                case 1: completion += ')'
                case 2: completion += ']'
                case 3: completion += '}'
                case 4: completion += '>'
        return completion

    def next_state(self, state: int, char: str) -> int:
        action = find(lambda ac: state in ac[0] and ac[1] == char, self.actions)
        return action[2] if action else -1


OPEN_DELIM = '([{<'
CLOSE_DELIM = ')]}>'

parser = ChunkParser(actions=[
    ([0, 1, 2, 3, 4], '(', 1),
    ([0, 1, 2, 3, 4], '[', 2),
    ([0, 1, 2, 3, 4], '{', 3),
    ([0, 1, 2, 3, 4], '<', 4),
    ([0, 1, 2, 3, 4], '[', 2),
    ([1], ')', 'pop'),
    ([2], ']', 'pop'),
    ([3], '}', 'pop'),
    ([4], '>', 'pop'),
])

Errors = List[Tuple[int, str]]
Completions = List[str]

def parse_lines(lines: List[str]) -> Tuple[Errors, Completions]:
    errors = []
    completions = []
    for line in lines:
        try:
            state = parser.parse(line)
            if len(state) > 1:
                completions.append(parser.complete(state))
        except ValueError as ex:
            errors.append((ex.args[-2], ex.args[-1]))
    return errors, completions

T = TypeVar('T', bound=Any)

def find(func: Callable[[T], bool], iterable: Iterable[T]) -> Optional[T]:
    """
    Finds the first element in `iterable` for which `func` returns `True`, if it exists.
    """
    return next((item for item in iterable if func(item)), None)


def read_input(input_path: str) -> List[str]:
    with open(f'day10/{input_path}', 'r') as inputfile:
        return list(map(lambda line: line.strip().rstrip('\n'), inputfile.readlines()))

def compute_score(errors: List[Tuple[int, str]]) -> int:
    return sum(list(map(lambda err: SCORES[err[1]], errors)))

COMPLETION_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def compute_completion_score(completions: List[str]) -> int:
    scores = []
    for completion in completions:
        score = 0
        for char in completion:
            score = score * 5 + COMPLETION_SCORES[char]
        scores.append(score)
    return sorted(scores)[len(completions) // 2]

def run(input_path: str, exp_score: int, exp_compl_score) -> None:
    lines = read_input(input_path)
    errors, completions = parse_lines(lines)
    total_score = compute_score(errors)
    print(f'There are {len(errors)} errors with a score of {total_score}')
    assert total_score == exp_score
    
    completion_score = compute_completion_score(completions)
    print(f'Total completion score: {completion_score}')
    assert completion_score == exp_compl_score
    


if __name__ == '__main__':
    run('sample_input.txt', 26397, 288957)
    run('input.txt', 268845, 4038824534)
