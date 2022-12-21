from tetris import Move, GameState
from algorithms.algorithm import TetrisAlgorithm


class TetrisAlgorithm(TetrisAlgorithm):
	def make_move(self, state: GameState) -> Move:
		# TODO: make tetris algorithm

		return Move(rotation=0, offset=0, hold=False)
