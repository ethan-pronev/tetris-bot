from game_types import Move, GameState
from algorithms.algorithm import Algorithm


class DownstackAlgorithm(Algorithm):
    def make_move(self, state: GameState) -> Move:
        # TODO: make downstack algorithm
        return Move(0, 0, hold=False)
        raise RuntimeError("Not implemented")
