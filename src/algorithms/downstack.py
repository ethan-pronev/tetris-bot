from game_types import Board, Move, GameState
from algorithms.algorithm import Algorithm
import algorithms.utils as utils


class DownstackAlgorithm(Algorithm):
    def __init__(self, left_col=0, right_col=9):
        self.left_col = left_col
        self.right_col = right_col

        self.hole_penalty = -300 # penalize holes
        self.height_penalty = [0,0,0,0,0,0,0,0,0,0,0,-10,-20,-40,-80,-250,-500,-1000,-2000,-2000,-2000] # penalize height
        self.height_diff_penalty = [-20,0,0,0,0,-30,-50,-60,-80,-100,-150,-200,-250,-300,-350,-400,-450,-500,-550,-600,-650] # penalize large height differences
        self.pit_penalty = [0,0,-10,-50,-50,-60,-80,-100,-120,-150,-180,-210,-250,-300,-350,-400,-450,-500,-550,-600,-650] # penalize long 1-wide pits

    def _score(self, board: Board) -> int:
        score = 0

        score += self.hole_penalty * utils.count_holes(board, self.left_col, self.right_col)

        heights = board.heights()[self.left_col:self.right_col+1]
        score += self.height_penalty[max(heights)]
        score += self.height_diff_penalty[max(heights) - min(heights)]

        pits = utils.count_pits(board, self.left_col, self.right_col)
        for pit_len, cnt in pits.items():
            score += cnt * self.pit_penalty[pit_len]
        # double-count pits on either end of the board since that seems be a common cause of failure
        left_diff = heights[self.left_col+1] - heights[self.left_col]
        if left_diff >= 2:
            score += self.pit_penalty[left_diff]
        right_diff = heights[self.right_col-1] - heights[self.right_col]
        if right_diff >= 2:
            score += self.pit_penalty[right_diff]

        return score

    def make_move(self, state: GameState) -> Move:
        boards = utils.generate_all_boards(state, depth=1, left_col=self.left_col, right_col=self.right_col, no_holes=False)

        mx = -float("inf")
        move = None
        for board, first_move in boards:
            score = self._score(board)
            if (score > mx):
                mx = score
                move = first_move

        return move
