
import functools as ft

from typing import List, Literal, Tuple, TypeVar, Union

Direction = Literal['down', 'forward', 'up']
Move = Tuple[Direction, int]
Position = Tuple[int, int]
PositionWithAim = Tuple[int, int]
PositionType = TypeVar('PositionType', bound=Union[Position, PositionWithAim])


def parse_move(move: str) -> Move:
    """
    Parses a submarine move from string.
    """
    direction, units = move.split()
    return direction, int(units)


def apply_moves(moves: List[Move], initial_pos: PositionType = (0, 0)) -> PositionType:
    """
    Applies all `moves` from `initial_pos`, selecting the appropriate strategy.
    """
    apply_move = apply_move_aim if len(initial_pos) == 3 else apply_move_noaim 
    return ft.reduce(apply_move, moves, initial_pos)


def apply_move_aim(pos: PositionWithAim, move: Move) -> PositionWithAim:
    """
    Applies `move` from `pos`, taking aim into account.
    """
    match move[0]:
        case 'down':
            return pos[0], pos[1], pos[2] + move[1]
        case 'forward':
            return pos[0] + move[1], pos[1] + pos[2] * move[1], pos[2]
        case 'up':
            return pos[0], pos[1], pos[2] - move[1]


def apply_move_noaim(pos: Position, move: Move) -> Position:
    """
    Applies `move` from `pos`.
    """
    match move[0]:
        case 'down':
            return pos[0], pos[1] + move[1]
        case 'forward':
            return pos[0] + move[1], pos[1]
        case 'up':
            return pos[0], pos[1] - move[1]


def read_input() -> List[Move]:
    with open('day2/input.txt', 'r') as inputfile:
        return list(map(parse_move, inputfile.readlines()))


if __name__ == '__main__':
    sample_moves = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
    actual_moves = read_input()
    
    assert apply_moves(sample_moves) == (15, 10)
    assert apply_moves(actual_moves) == (1925, 879)
    print(f'Horizontal by depth: {1925 * 879}')

    assert apply_moves(sample_moves, initial_pos=(0, 0, 0)) == (15, 60, 10)
    assert apply_moves(actual_moves, initial_pos=(0, 0, 0)) == (1925, 908844, 879)
    print(f'Horizontal by depth: {1925 * 908844}')
