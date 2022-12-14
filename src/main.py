from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint_tetris import SprintTetrisStrategy


def main():
    controller = GameController(
        pps=1,
        client=JstrisClient(),
        strategy=SprintTetrisStrategy(),
        room="join",
        join_info="CK4FRH"
    )

    controller.start()


if __name__ == "__main__":
    main()
