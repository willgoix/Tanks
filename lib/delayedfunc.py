import threading
import time

queue = []


def cancelAll():
	for funcs in queue:
		funcs.cancel()
	queue.clear()

class DelayedFunc:

	def __init__(self, function, delay):
		self.function = function
		self.delay = delay

		def func():
			while self.delay > 0 and self.thread.isAlive:
				self.delay -= 1
				time.sleep(1)

				if self.delay <= 0 and self.thread.isAlive:
					self.function()
					self.cancel()

		self.thread = threading.Thread(target=func)
		self.thread.start()

		queue.append(self)

	def cancel(self):
		self.thread.isAlive = False
