from abc import ABC, abstractmethod

from tetris import Move, GameState


class TetrisAlgorithm(ABC):
    @abstractmethod
    def make_move(self, state: GameState) -> Move:
        pass
