from datetime import datetime, timedelta
# import multiprocessing
# import time
from io import BytesIO
from sys import exit
# from numpy import array as np_array
from PIL.Image import open as open_image
from ppadb.client import Client
# from threading import Thread


class Main:
	def __init__(self):
		self.adb = Client()
		self.device = self.adb.devices()[0] if self.adb.devices() else exit("No Device Found")
		self.shell = self.device.shell
		self.color_options = self.color_needed = self.screen = None
		# self.wr, self.hr = (248, 518, 788), (1296, 1584)
		# self.dimensions = ((w, h) for w in self.wr for h in self.hr)
		self.dimensions = ((248, 1296), (248, 1584), (518, 1296), (518, 1584), (788, 1296), (788, 1584))
		self.refresh_screen()
		self.set_color_options()

	def refresh_screen(self):
		self.screen = open_image(BytesIO(self.device.screencap()))
		self.color_needed = self.screen.getpixel((600, 540))
		# print("Color Needed :", self.color_needed)

	def set_color_options(self):
		if self.screen is not None:
			# self.color_options = [(self.screen[h][w], w, h) for h in self.hr for w in self.wr]
			self.color_options = tuple(self.screen.getpixel((w, h)) for w, h in self.dimensions)
			print(f"Color Options : {self.color_options}")
			return

	def index_of_color(self):
		return self.dimensions[self.color_options.index(self.color_needed)]

	def start_loop(self, game_time=44):
		end = now() + timedelta(0, game_time)
		x, y = self.index_of_color()
		# self.shell(f"input swipe {x+10} {y} {x} {y+10}")
		self.shell(f"input {x+10} {y}")
		score = 1
		while now() < end:
			self.refresh_screen()
			x, y = self.index_of_color()
			# self.shell(f"input swipe {x + 5} {y} {x+30} {y}")
			self.shell(f"input tap {x + 5} {y}")
			# score = score + 1
		print(score)


# def colored(r, g, b, text):
# 	return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

input("Start??: ")
now = datetime.now
started = now()
game = Main()
game.start_loop()

print(f"End took {datetime.now() - started}")
# 56, 56, 48, 44
