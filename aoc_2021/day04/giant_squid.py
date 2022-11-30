
import dataclasses
import itertools as it

from typing import Any, Callable, Dict, List, Optional, Set, Tuple

BingoNumbers = List[int]

@dataclasses.dataclass
class BingoBoard:
    id: int
    """
    Board identifier.
    """
    lines: List[List[int]]
    """
    Lines of numbers for the Bingo Board.
    """
    __numbers_by_row: Dict[int, int] = dataclasses.field(default_factory=dict)
    """
    Mapping of items to their row on the board. 
    """
    __marked: Set[int] = dataclasses.field(default_factory=set)
    """
    Marked items for this board.
    """
    __marked_row_col: Dict[str, int] = dataclasses.field(default_factory=dict)
    """
    Marked counts for each row/col.
    """
    __is_complete: bool = False
    """
    Tracks bingo completion.
    """

    def bingo(self) -> bool:
        """
        Checks if any line has all 5 elements marked.
        """
        if not self.__is_complete:
            self.__is_complete = any(list(map(lambda value: value == 5, self.__marked_row_col.values())))
        return self.__is_complete
    
    def mark(self, number: int) -> None:
        """
        Marks `number` on the board.
        """
        if number not in self.__numbers_by_row:
            raise ValueError('No cheating!')
        row = self.__numbers_by_row[number]
        col = self.lines[row].index(number)
        self.__marked.add(number)
        self.__marked_row_col[f'r{row}'] += 1
        self.__marked_row_col[f'c{col}'] += 1

    def is_marked(self, number: int) -> bool:
        """
        Checks if `number` is marked.
        """
        return number in self.__marked

    def unmarked_total(self) -> int:
        """
        Computes the sum of unmarked items on the board.
        """
        return sum(filter(neg(self.is_marked), list(it.chain(*self.lines))))

    def print_status(self) -> None:
        print(self.__marked_row_col)
        print(f'--- Board #{self.id} -----------')
        for key, marked in self.__marked_row_col.items():
            what = 'Row' if key.startswith('r') else 'Col'
            print(f'{what} {key.replace("r", "").replace("c", "")}: {marked} items')
        print('------------------------')
        print()
    
    def __repr__(self) -> str:
        board = f'--- Board #{self.id} -----------\n'
        for line in self.lines:
            board += ' '.join(map(lambda num: f'{num:2d}', line))
            board += '\n'
        board += '------------------------\n'
        return board

    def __post_init__(self) -> None:
        self.__numbers_by_row = { num: row_num for row_num, row 
            in enumerate(self.lines) for num in row }
        self.__marked_row_col = dict()
        for i in range(len(self.lines)):
            self.__marked_row_col[f'r{i}'] = 0
            self.__marked_row_col[f'c{i}'] = 0

    def __contains__(self, item: Any) -> bool:
        """
        Checks if `item` is in the board.
        """
        return item in self.__numbers_by_row


def neg(func: Callable[..., bool]) -> Callable[..., bool]:
    def negated_func(*args, **kwargs) -> bool:
        return not func(*args, **kwargs)
    return negated_func


def read_input(filename: str) -> Tuple[BingoNumbers, List[BingoBoard]]:
    """
    Reads bingo boards from file.
    """
    with open(f'day04/{filename}', 'r') as bingofile:
        lines = bingofile.readlines()
    numbers = list(map(int, lines[0].strip('\n').split(',')))
    boards = []
    board = []
    for i, line in enumerate(lines[2:]):
        if not line.strip():
            continue
        board.append(list(map(int, line.split())))
        if i % 6 == 4:
            boards.append(BingoBoard(lines=board, id=len(boards) + 1))
            board = []
    return numbers, boards


def find_board(numbers: BingoNumbers, boards: List[BingoBoard], best: bool = True) -> Tuple[Optional[BingoBoard], int]:
    """
    Finds the board that wins first in `boards`, given `numbers`.
    If `best` is `True`, finds the first winning board; otherwise, finds the last one.
    If more than one board win on the same round, returns the highest-scoring board.
    """
    winners: List[Tuple[BingoBoard, int, int]] = []
    for i, number in enumerate(numbers):
        for board in filter(lambda b: number in b and not b.bingo(), boards):
            board.mark(number)
            if board.bingo():
                winners.append((board, i+1, number))
        
        # Checks if "best" or "worst" board strategy has been chosen
        # and picks the board accordingly
        if best:
            if winners:
                scores = list(map(lambda winner: compute_score(*winner), winners))
                return max(zip(map(lambda w: w[0], winners), scores), key=lambda o: o[1])
    if not best:
        winner = winners[-1]
        return winner[0], compute_score(*winner)
    return None, -1

def compute_score(board: BingoBoard, round: int, winning_number: int) -> int:
    """"""
    return board.unmarked_total() * winning_number


def main(inputfile: str, expected_score: int, best: bool= True) -> None:
    numbers, boards = read_input(inputfile)
    board, score = find_board(numbers, boards, best=best)
    print(f'The {"best" if best else "worst"} board is Board #{board.id} with a score of {score}')
    assert score == expected_score

if __name__ == '__main__':
    main('sample_input.txt', 4512, best=True)
    main('input.txt', 10680, best=True)

    main('sample_input.txt', 1924, best=False)
    main('input.txt', 31892, best=False)
