from tetris import Move, GameState
from strategies.strategy import TetrisStrategy


class SprintTetrisStrategy(TetrisStrategy):
	def __init__(self):
		pass

	def make_move(self, state: GameState) -> Move:
		# TODO: make algorithm to determine next move from given state

		# print(f"queue: {state.upcoming}")
		# print(f"current: {state.current}")
		# print(f"held: {state.held}")
		# print("board:")
		# for row in state.board[::-1]:
		# 	print("".join(["O" if a else "." for a in row]))

		return Move(rotation=0, offset=0, hold=False)
