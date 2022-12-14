from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from clients.client import TetrisClient
from tetris import Piece, Move, GameState


class JstrisClient(TetrisClient):
	def __init__(self):
		self.page = webdriver.Chrome()
		self.page.get("https://jstris.jezevec10.com/")

	def _click_buttons(self, ids):
		for id in ids:
			button = self.page.find_element(By.ID, id)
			button.click()
			time.sleep(1)

	def create_room(self):
		self._click_buttons(["lobby", "createRoomButton", "isPrivate", "create", "lobby", "editRoomButton"])

		gravity_field = self.page.find_element(By.ID, "gravityLvl")
		gravity_field.send_keys([Keys.BACK_SPACE, "0"])

		self._click_buttons(["create"])

		link = self.page.find_element(By.CLASS_NAME, "joinLink")
		print(f"Room URL: {link.text}")

	def join_room(self, code):
		self.page.get(f"https://jstris.jezevec10.com/join/{code}")

	def get_game_state(self) -> GameState:
		# TODO: get game state from jstris screenshot

		return GameState([], [Piece.I], None)

	def play_move(self, move: Move):
		body = self.page.find_element(By.CSS_SELECTOR, "body")

		keys = []

		if move.hold:
			keys.append("c")

		else:
			if move.rotation == 90:
				keys.append(Keys.UP)
			elif move.rotation== 180:
				keys.append("a")
			elif move.rotation == 270:
				keys.append("z")

			if move.offset > 0:
				keys += [Keys.RIGHT for _ in range(move.offset)]
			elif move.offset < 0:
				keys += [Keys.LEFT for _ in range(-move.offset)]

			keys.append(Keys.SPACE)

		body.send_keys(keys)
