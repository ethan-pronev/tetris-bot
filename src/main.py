from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint_tetris import SprintTetrisStrategy


def main():
    controller = GameController(
        pps=5.5,
        client=JstrisClient(),
        strategy=SprintTetrisStrategy(),
        room="join",
        join_info="ZNWSJ6"
    )

    controller.start()


if __name__ == "__main__":
    main()
