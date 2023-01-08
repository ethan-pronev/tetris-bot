from typing import Dict, List, Tuple

from game_types import Board, Piece, Move, GameState


def _get_boards(board: Board, left_col: int, right_col: int, pieces: List[Piece], first_move=None, first_hold=False) -> List[Tuple[Board, Move]]:
    piece = pieces[0]
    boards = []

    placements = [] # rotation-position tuples
    if piece in [Piece.L, Piece.J, Piece.T]:
        placements = [(rot, pos) for rot in [0,180] for pos in range(left_col, right_col-1)] + [(rot, pos) for rot in [90,270] for pos in range(left_col, right_col)]
    elif piece in [Piece.S, Piece.Z]:
        placements = [(0, pos) for pos in range(left_col, right_col-1)] + [(90, pos) for pos in range(left_col, right_col)]
    elif piece == Piece.O:
        placements = [(0, pos) for pos in range(left_col, right_col)]
    elif piece == Piece.I:
        placements = [(0, pos) for pos in range(left_col, right_col-2)] + [(90, pos) for pos in range(left_col, right_col+1)]
    
    for rotation, position in placements:
        new_board = Board([row[:] for row in board.rows])
        new_board.drop_piece(piece, rotation, position)

        if first_move is None:
            move = Move(piece, rotation, position, hold=first_hold)
        else:
            move = Move(first_move.piece, first_move.rotation, first_move.position, first_move.hold)

        if len(pieces) == 1:
            boards.append((new_board, move))
        else:
            boards += _get_boards(new_board, left_col, right_col, pieces[1:], first_move=move)
    
    return boards


def generate_all_boards(state: GameState, depth: int, left_col: int=0, right_col: int=9, no_holes: bool=False) -> List[Tuple[Board, Move]]:
    all_boards = []

    hold_seqs = [bin(i)[3:] for i in range(2**depth, 2**(depth+1))]
    for seq in hold_seqs:
        current = state.current
        held = state.held
        upcoming = state.upcoming.copy()

        pieces = []
        for move in seq:
            if move == "0": # don't hold
                pieces.append(current)
                current = upcoming[0]
                upcoming.pop(0)
            else: # hold
                if held is None:
                    held = current
                    pieces.append(upcoming[0])
                    current = upcoming[1]
                    upcoming.pop(0)
                    upcoming.pop(0)
                else:
                    pieces.append(held)
                    held = current
                    current = upcoming[0]
                    upcoming.pop(0)

        first_hold = True if seq[0] == "1" else False

        all_boards += _get_boards(state.board, left_col, right_col, pieces, first_hold=first_hold)

    return all_boards


def count_holes(board: Board, left_col: int=0, right_col: int=9) -> int:
    holes = 0

    for i, height in enumerate(board.heights()[left_col:right_col+1]):
        for j in range(height):
            if board.rows[j][i] == False:
                holes += 1
    
    return holes


def count_pits(board: Board, left_col: int=0, right_col: int=9) -> Dict[int, int]:
    pits = dict.fromkeys(range(2,21), 0)

    heights = board.heights()[left_col:right_col+1]
    for i in range(0, len(heights)):
        left = heights[i] if i == left_col else heights[i-1]
        right = heights[i] if i == right_col else heights[i+1]

        pit_height = min(left - heights[i], right - heights[i])
        if pit_height >= 2:
            pits[pit_height] += 1
    
    return pits
