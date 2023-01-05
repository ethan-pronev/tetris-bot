from game_types import Move, GameState
from strategies.strategy import Strategy
from algorithms.tetris import TetrisAlgorithm
from algorithms.downstack import DownstackAlgorithm


class PvPTetrisStrategy(Strategy):
    def __init__(self, downstack_limit):
        assert(0 <= downstack_limit <= 20)
        self.downstack_limit = downstack_limit

        self. tetris_algo: TetrisAlgorithm = TetrisAlgorithm()
        self. downstack_algo: DownstackAlgorithm = DownstackAlgorithm()

    def make_move(self, state: GameState) -> Move:
        if max(state.board.heights()) >= self.downstack_limit:
            return self.downstack_algo.make_move(state)
        else:
            return self.tetris_algo.make_move(state)
