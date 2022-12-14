import threading as th
import time


class GameController():
    def __init__(self, room, pps, client, strategy):
        self.game_active = False
        self.pps = pps
        self.client = client
        self.strategy = strategy

        if room == "host":
            self.client.create_room()
        else:
            raise RuntimeError("Invalid room type")

    def key_capture_thread(self):
        input("press ENTER to stop playing:")
        self.game_active = False

    def run_game(self):
        th.Thread(target=self.key_capture_thread, args=(), name="key_capture_thread", daemon=True).start()
        while self.game_active:
            state = self.client.get_game_state()
            move = self.strategy.get_move(state)
            self.client.play_move(move)
            time.sleep(1 / self.pps)

    def start(self):
        while True:
            sig = input("Press ENTER to start playing, or q to quit: ")
            if sig == "q":
                return
            elif sig == "":
                self.game_active = True
                self.run_game()
