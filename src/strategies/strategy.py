from abc import ABC, abstractmethod

from game_types import Move, GameState


# A strategy determines the overall way the bot will play. Depending on characteristics of the game state, a strategy can choose between several algorithms to make the next move
class Strategy(ABC):
    @abstractmethod
    def make_move(self, state: GameState) -> Move:
        pass
