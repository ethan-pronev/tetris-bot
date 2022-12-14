from tetris import Move, GameState
from strategies.strategy import TetrisStrategy


class SprintTetrisStrategy(TetrisStrategy):
	def __init__(self):
		pass

	def make_move(self, state: GameState) -> Move:
		# TODO: make algorithm to determine next move from given state

		return Move(rotation=0, offset=0)
