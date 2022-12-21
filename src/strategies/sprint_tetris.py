from tetris import Move, GameState
from strategies.strategy import TetrisStrategy
from algorithms.tetris import TetrisAlgorithm


class SprintTetrisStrategy(TetrisStrategy):
	def __init__(self):
		self. tetris_algo: TetrisAlgorithm = TetrisAlgorithm()

	# This strategy is meant for sprint mode, so no need to worry about garbage/downstacking/etc.
	def make_move(self, state: GameState) -> Move:
		return self.tetris_algo.make_move(state)
