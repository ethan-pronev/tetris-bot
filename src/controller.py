from pynput import keyboard
import time
from typing import Literal

from game_types import Piece, Move
from clients.client import Client
from strategies.strategy import Strategy


class GameController():
    def __init__(self, pps, client: Client, strategy: Strategy, room: Literal["host", "join"], join_info=None):
        self.game_active = False
        self.quit_game = False

        self.pps = pps
        self.client = client
        self.strategy = strategy

        if room == "host":
            self.client.create_room()
        elif room == "join":
            self.client.join_room(join_info)
        else:
            raise RuntimeError("Invalid room type")

    def on_press(self, key):
        try:
            if key.char == "s":
                if self.game_active:
                    self.game_active = False
                    print("Stopping...")
                else:
                    self.game_active = True
                    print("Starting...")
            elif key.char == "q":
                self.quit_game = True
                print("Quitting...")
        except:
            pass

    def start(self):
        print("Press 's' to start/stop, and 'q' to quit")
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        while True:
            if self.quit_game:
                self.client.leave_room()
                return
            if not self.game_active:
                continue

            start_time = time.time()

            state = self.client.get_game_state()
            if state is None:
                self.game_active = False
                self.client.play_move(Move(Piece.I, 0, 3)) # if we've reached the very top of the board, the next piece will spawn above the board, so drop it just in case
                continue

            move = self.strategy.make_move(state)
            self.client.play_move(move)

            delta = time.time() - start_time
            sleep_len = 1 / self.pps - delta
            if sleep_len > 0:
                time.sleep(sleep_len)
