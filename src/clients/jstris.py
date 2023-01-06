import base64
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from clients.client import Client
from game_types import Board, Piece, Move, GameState

_PIECE_POSITIONS = {
	Piece.L: {
		0: 3,
		90: 4,
		180: 3,
		270: 3,
	},
	Piece.J: {
		0: 3,
		90: 4,
		180: 3,
		270: 3,
	},
	Piece.S: {
		0: 3,
		90: 4,
		180: 3,
		270: 3,
	},
	Piece.Z: {
		0: 3,
		90: 4,
		180: 3,
		270: 3,
	},
	Piece.O: {
		0: 4,
		90: 4,
		180: 4,
		270: 4,
	},
	Piece.I: {
		0: 3,
		90: 5,
		180: 3,
		270: 4,
	},
	Piece.T: {
		0: 3,
		90: 4,
		180: 3,
		270: 3,
	},
}


class JstrisClient(Client):
	def __init__(self, headless=False):
		chrome_options = Options()
		if headless:
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("window-size=1920,1080")

		self.page = webdriver.Chrome(options=chrome_options)
		self.page.get("https://jstris.jezevec10.com/")

	def _click_buttons(self, ids, waitTime=1):
		for id in ids:
			time.sleep(waitTime)
			button = self.page.find_element(By.ID, id)
			button.click()
	
	def _get_piece_from_pixels(self, pixels) -> Piece | None:
		if (227,91,2,255) in pixels:
			return Piece.L
		elif (33,65,198,255) in pixels:
			return Piece.J
		elif (89,177,1,255) in pixels:
			return Piece.S
		elif (215,15,55,255) in pixels:
			return Piece.Z
		elif (15,155,215,255) in pixels:
			return Piece.I
		elif (227,159,2,255) in pixels:
			return Piece.O
		elif (175,41,138,255) in pixels:
			return Piece.T
		elif (153,153,153,255) in pixels:
			return "Garbage"
		else:
			return None

	def create_room(self):
		self._click_buttons(["lobby", "createRoomButton", "isPrivate", "more_adv"])

		gravity_field = self.page.find_element(By.ID, "gravityLvl")
		gravity_field.send_keys([Keys.BACK_SPACE, "0"])

		self._click_buttons(["create"])

		time.sleep(2)
		link = self.page.find_element(By.CLASS_NAME, "joinLink")
		print(f"Room URL: {link.text}")

	def join_room(self, code):
		self.page.get(f"https://jstris.jezevec10.com/join/{code}")

	def get_game_state(self) -> GameState:
		screenshot = self.page.find_element(By.ID, "main").screenshot_as_base64
		image = Image.open(BytesIO(base64.b64decode(screenshot)))

		board = []
		for i in range(19,0,-1):
			row = []
			for j in range(10):
				pixel = image.getpixel((24*j+118,24*i+12))
				row.append(self._get_piece_from_pixels([pixel]) is not None)
			board.append(row)
		board.append([False for _ in range(10)]) # to not count current piece at top

		current = self._get_piece_from_pixels([image.getpixel((214,12))])

		queue = []
		for i in range(5):
			queue.append(self._get_piece_from_pixels(
				[
					image.getpixel((412,72*i+36)),
					image.getpixel((412,72*i+60)),
				]
			))
		
		hold = self._get_piece_from_pixels(
			[
				image.getpixel((36,36)),
				image.getpixel((36,60)),
			]
		)

		# in jstris we know the game is finished when no current piece is detected (board is greyed out)
		if current is None:
			return None

		return GameState(Board(board), current, queue, hold)

	def play_move(self, move: Move):
		body = self.page.find_element(By.CSS_SELECTOR, "body")

		keys = []

		if move.hold:
			keys.append("c")

		if move.rotation == 90:
			keys.append(Keys.UP)
		elif move.rotation== 180:
			keys.append("a")
		elif move.rotation == 270:
			keys.append("z")

		offset = move.position - _PIECE_POSITIONS[move.piece][move.rotation]
		if offset > 0:
			keys += [Keys.RIGHT for _ in range(offset)]
		elif offset < 0:
			keys += [Keys.LEFT for _ in range(-offset)]

		keys.append(Keys.SPACE)

		body.send_keys(keys)
