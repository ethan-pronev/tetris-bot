from enum import Enum
from typing import List


class Piece(Enum):
    L = 1
    J = 2
    S = 3
    Z = 4
    O = 5
    I = 6
    T = 7


class Move():
    def __init__(self, rotation, offset, hold=False):
        assert(rotation in [0, 90, 180, 270])

        self.rotation = rotation
        self.offset = offset
        self.hold = hold


class GameState():
    def __init__(self, board, current: Piece, upcoming: List[Piece], held: Piece | None = None):
        self.board = board
        self.current = current
        self.upcoming = upcoming
        self.held = held
