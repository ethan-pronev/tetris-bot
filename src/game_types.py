from enum import Enum
from typing import List


class Board():
    def __init__(self, rows):
        self.rows = rows
        self.cols = [[row[j] for row in rows] for j in range(len(rows[0]))]
    
    def height(self, col):
        assert(0 <= col < 10)
        
        for i in range(len(self.cols[col])-1, -1, -1):
            if self.cols[col][i]:
                return i + 1
        return 0
    
    def heights(self):
        return [self.height(i) for i in range(10)]


class Piece(Enum):
    L = 1
    J = 2
    S = 3
    Z = 4
    O = 5
    I = 6
    T = 7


class Move():
    def __init__(self, rotation: int, offset: int, hold: bool=False):
        assert(rotation in [0, 90, 180, 270])

        self.rotation = rotation
        self.offset = offset
        self.hold = hold


class GameState():
    def __init__(self, board: Board, current: Piece, upcoming: List[Piece], held: Piece | None = None):
        self.board = board
        self.current = current
        self.upcoming = upcoming
        self.held = held
