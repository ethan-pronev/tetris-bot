from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint import SprintStrategy


def main():
    controller = GameController(
        pps=4.5,
        client=JstrisClient(headless=False),
        strategy=SprintStrategy(),
        room="join",
        join_info="XT0658"
    )

    controller.start()


if __name__ == "__main__":
    main()
