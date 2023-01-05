from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint import SprintStrategy


def main():
    controller = GameController(
        pps=1,
        client=JstrisClient(headless=False),
        strategy=SprintStrategy(),
        room="join",
        join_info="OLYTFL"
    )

    controller.start()


if __name__ == "__main__":
    main()
