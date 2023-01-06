from game_types import Board, Move, GameState
from algorithms.algorithm import Algorithm
import algorithms.utils as utils


class DownstackAlgorithm(Algorithm):
    def _count_holes(self, board: Board) -> int:
        holes = 0

        for i, height in enumerate(board.heights()):
            for j in range(height):
                if board.rows[j][i] == False:
                    holes += 1
        
        return holes

    def _count_pits(self, board: Board) -> int:
        pits = 0

        heights = board.heights()
        for i in range(1, len(heights) - 1):
            if heights[i-1] - heights[i] >= 3 and heights[i+1] - heights[i] >=3:
                pits += 1
        
        return pits


    def _score(self, board: Board) -> int:
        score = 0

        score += -200 * self._count_holes(board) # penalize holes

        max_height = max(board.heights())
        score += -10 * max_height # penalize height
        if max_height > 10:
            score += -20 * max_height

        score += -30 * self._count_pits(board) # penalize long 1-wide pits

        # holes = self._count_holes(board)
        # height = max(board.heights())
        # score += -100 * holes + -10 * height
        # board.print()
        # print(f"holes: {holes}, height: {height}, score: {score}")
        # print("")

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
