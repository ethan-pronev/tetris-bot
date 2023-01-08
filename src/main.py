from controller import GameController
from clients.jstris import JstrisClient
from strategies.sprint import SprintStrategy


def main():
    controller = GameController(
        pps=10,
        client=JstrisClient(headless=False),
        strategy=SprintStrategy(),
        room="join",
        join_info="XGD4VF"
    )

    controller.start()


if __name__ == "__main__":
    main()
