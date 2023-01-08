from abc import ABC, abstractmethod

from game_types import Move, GameState


class Client(ABC):
    @abstractmethod
    def create_room(self):
        pass

    @abstractmethod
    def join_room(self, info):
        pass

    @abstractmethod
    def leave_room(self):
        pass

    @abstractmethod
    def get_game_state(self) -> GameState | None:
        pass

    @abstractmethod
    def play_move(self, move: Move):
        pass
