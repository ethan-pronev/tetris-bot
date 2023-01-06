import multiprocessing as mp
import time
from typing import Literal

from game_types import Piece, Move
from clients.client import Client
from strategies.strategy import Strategy


class GameController():
    def __init__(self, pps, client: Client, strategy: Strategy, room: Literal["host", "join"], join_info=None):
        self.game_active = False
        self.pps = pps
        self.client = client
        self.strategy = strategy

        if room == "host":
            self.client.create_room()
        elif room == "join":
            self.client.join_room(join_info)
        else:
            raise RuntimeError("Invalid room type")

    def key_capture_thread(self):
        try:
            input("press ENTER to stop playing: ")
            # self.game_active = False
        except: # in case this process is killed below, ignore EOF error
            return

    def run_game(self):
        proc = mp.Process(target=self.key_capture_thread, args=(), name="key_capture_thread", daemon=True)
        proc.start()
        while self.game_active:
            start_time = time.time()

            state = self.client.get_game_state()
            if state is None:
                proc.kill()
                self.game_active = False
                self.client.play_move(Move(Piece.I, 0, 3)) # if we've reached the very top of the board, the next piece will spawn above the board, so drop it just in case
                print("")
                return

            move = self.strategy.make_move(state)
            self.client.play_move(move)

            delta = time.time() - start_time
            sleep_len = 1 / self.pps - delta
            if sleep_len > 0:
                time.sleep(sleep_len)

    def start(self):
        while True:
            sig = input("Press ENTER to start playing, or q to quit: ")
            if sig == "q":
                return
            elif sig == "":
                self.game_active = True
                self.run_game()
