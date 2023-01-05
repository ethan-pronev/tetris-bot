from game_types import Move, GameState
from strategies.strategy import Strategy
from algorithms.downstack import DownstackAlgorithm


class SprintStrategy(Strategy):
	def __init__(self):
		self. downstack_algo: DownstackAlgorithm = DownstackAlgorithm()

	# This strategy is meant for sprint mode, so no need to worry about garbage/tetrises/etc.
	def make_move(self, state: GameState) -> Move:
		return self.downstack_algo.make_move(state)
