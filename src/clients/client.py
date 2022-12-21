from abc import ABC, abstractmethod

from tetris import Move, GameState


class TetrisClient(ABC):
    @abstractmethod
    def create_room(self):
        pass

    @abstractmethod
    def join_room(self, info):
        pass

    @abstractmethod
    def get_game_state(self) -> GameState:
        pass

    @abstractmethod
    def play_move(self, move: Move):
        pass
