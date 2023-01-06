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


_PIECE_SHAPES = {
    Piece.L: {
        0: [[True, True, True], [False, False, True]],
        90: [[True, True], [True, False], [True, False]],
        180: [[True, False, False], [True, True, True]],
        270: [[False, True], [False, True], [True, True]]
    },
    Piece.J: {
        0: [[True, True, True], [True, False, False]],
        90: [[True, False], [True, False], [True, True]],
        180: [[False, False, True], [True, True, True]],
        270: [[True, True], [False, True], [False, True]]
    },
    Piece.S: {
        0: [[True, True, False], [False, True, True]],
        90: [[False, True], [True, True], [True, False]],
        180: [[True, True, False], [False, True, True]],
        270: [[False, True], [True, True], [True, False]]
    },
    Piece.Z: {
        0: [[False, True, True], [True, True, False]],
        90: [[True, False], [True, True], [False, True]],
        180: [[False, True, True], [True, True, False]],
        270: [[True, False], [True, True], [False, True]]
    },
    Piece.O: {
        0: [[True, True], [True, True]],
        90: [[True, True], [True, True]],
        180: [[True, True], [True, True]],
        270: [[True, True], [True, True]]
    },
    Piece.I: {
        0: [[True, True, True, True]],
        90: [[True], [True], [True], [True]],
        180: [[True, True, True, True]],
        270: [[True], [True], [True], [True]]
    },
    Piece.T: {
        0: [[True, True, True], [False, True, False]],
        90: [[True, False], [True, True], [True, False]],
        180: [[False, True, False], [True, True, True]],
        270: [[False, True], [True, True], [False, True]]
    }
}


class Board():
    def __init__(self, rows: List[List[bool]]):
        self.rows = rows
        self.cols = [[row[j] for row in rows] for j in range(len(rows[0]))]

    def __str__(self):
        s = ""
        for row in self.rows:
            for tile in row:
                s += "1" if tile else "0"
        return s

    def print(self):
        for row in reversed(self.rows):
            print("".join(["." if tile == False else "O" for tile in row]))
    
    def height(self, col):
        assert(0 <= col < 10)
        
        for i in range(len(self.cols[col])-1, -1, -1):
            if self.cols[col][i]:
                return i + 1
        return 0
    
    def heights(self):
        return [self.height(i) for i in range(10)]

    def drop_piece(self, piece: Piece, rotation: int, position: int):
        shape = _PIECE_SHAPES[piece][rotation]

        # find position that piece will be dropped
        last_overlap = -1
        for row in range(20 - len(shape)):
            for r in range(len(shape)):
                for c in range(len(shape[0])):
                    if self.rows[row + r][position + c] and shape[r][c]:
                        last_overlap = row
        
        # add piece to board
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                self.rows[last_overlap + 1 + r][position + c] = self.rows[last_overlap + 1 + r][position + c] or shape[r][c]
        
        # clear any full lines
        new_rows = []
        for row in self.rows:
            if False in row:
                new_rows.append(row)

        self.rows = new_rows + [[False for _ in range(10)] for _ in range(20-len(new_rows))]
        self.cols = [[row[j] for row in self.rows] for j in range(len(self.rows[0]))]


class Move():
    def __init__(self, piece: Piece, rotation: int, position: int, hold: bool=False):
        assert(rotation in [0, 90, 180, 270])
        assert(position in range(10))

        self.piece = piece # stored here in case the client needs it to calculate piece offsets, etc.
        self.rotation = rotation
        self.position = position # represents the leftmost column taken up by the piece after rotating
        self.hold = hold # whether or not this move involves swapping to the held piece


class GameState():
    def __init__(self, board: Board, current: Piece, upcoming: List[Piece], held: Piece | None = None):
        self.board = board
        self.current = current
        self.upcoming = upcoming
        self.held = held
