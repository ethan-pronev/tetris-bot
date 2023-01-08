from game_types import Board, Move, GameState
from algorithms.algorithm import Algorithm
import algorithms.utils as utils


class DownstackAlgorithm(Algorithm):
    def __init__(self):
        self.hole_penalty = -300 # penalize holes
        self.height_penalty = [0,0,0,0,0,0,0,0,0,0,0,-10,-20,-40,-80,-250,-500,-1000,-2000,-2000,-2000] # penalize height
        self.height_diff_penalty = [-20,0,0,0,0,-30,-50,-60,-80,-100,-150,-200,-250,-300,-350,-400,-450,-500,-550,-600,-650] # penalize large height differences
        self.pit_penalty = [0,0,-10,-50,-50,-60,-80,-100,-120,-150,-180,-210,-250,-300,-350,-400,-450,-500,-550,-600,-650] # penalize long 1-wide pits

    def _score(self, board: Board) -> int:
        score = 0

        score += self.hole_penalty * utils.count_holes(board)

        heights = board.heights()
        score += self.height_penalty[max(heights)]
        score += self.height_diff_penalty[max(heights) - min(heights)]

        pits = utils.count_pits(board)
        for pit_len, cnt in pits.items():
            score += cnt * self.pit_penalty[pit_len]

        return score

    def make_move(self, state: GameState) -> Move:
        boards = utils.generate_all_boards(state, depth=1, no_holes=False)

        mx = -float("inf")
        move = None
        for board, first_move in boards:
            score = self._score(board)
            if (score > mx):
                mx = score
                move = first_move

        return move
