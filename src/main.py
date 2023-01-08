from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint import SprintStrategy
from strategies.pvp_tetris import PvPTetrisStrategy


def main():
    controller = GameController(
        pps=4,
        client=JstrisClient(headless=False),
        # strategy=SprintStrategy(),
        strategy=PvPTetrisStrategy(12, 3),
        room="join",
        join_info="ERW1PV"
    )

    controller.start()


if __name__ == "__main__":
    main()
