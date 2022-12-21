from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint_tetris import SprintTetrisStrategy


def main():
    controller = GameController(
        pps=1,
        client=JstrisClient(headless=False),
        strategy=SprintTetrisStrategy(),
        room="join",
        join_info="3RD3GN"
    )

    controller.start()


if __name__ == "__main__":
    main()
