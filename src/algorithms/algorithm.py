from abc import ABC, abstractmethod

from game_types import Move, GameState


class Algorithm(ABC):
    @abstractmethod
    def make_move(self, state: GameState) -> Move:
        pass
