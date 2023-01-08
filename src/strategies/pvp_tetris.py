from game_types import Piece, Move, GameState
from strategies.strategy import Strategy
from algorithms.downstack import DownstackAlgorithm
import algorithms.utils as utils


class PvPTetrisStrategy(Strategy):
    def __init__(self, buildup_limit, downstack_limit):
        assert(0 <= downstack_limit <= 20)
        self.buildup_limit = buildup_limit # keep playing tetrises until this height is reached, then downstack
        self.downstack_limit = downstack_limit # keep downstacking until below this height, then play tetrises
        self.building_up = True

        self. buildup_algo: DownstackAlgorithm = DownstackAlgorithm(0, 8)
        self. downstack_algo: DownstackAlgorithm = DownstackAlgorithm()

    def _tetris_ready(self, state: GameState) -> bool:
        if state.current != Piece.I and state.held != Piece.I:
            return False

        right_height = state.board.height(9)
        if right_height > 16:
            return False

        ready = True
        for row in range(right_height, right_height+4):
            if state.board.rows[row] != [True for _ in range(9)] + [False]:
                ready = False

        return ready


    def make_move(self, state: GameState) -> Move:
        max_height = max(state.board.heights())
        if self.building_up and max_height >= self.buildup_limit:
            self.building_up = False
        elif not self.building_up and max_height <= self.downstack_limit:
            self.building_up = True

        # only build if there are no holes
        if utils.count_holes(state.board) != 0:
            self.building_up = False

        if self.building_up:
            if self._tetris_ready(state): # only place I if it is a tetris
                hold = False if state.current == Piece.I else True
                return Move(Piece.I, 90, 9, hold)
            else:
                return self.buildup_algo.make_move(state)
        else:
            return self.downstack_algo.make_move(state)
