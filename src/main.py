from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint_tetris import SprintTetrisStrategy


def main():
    controller = GameController(
        room="host",
        pps=1,
        client=JstrisClient(),
        strategy=SprintTetrisStrategy()
    )

    controller.start()


if __name__ == "__main__":
    main()
