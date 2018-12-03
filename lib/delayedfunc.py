import threading, time

class DelayedFunc:

	def __init__(self, function, delay):
		self.function = function
		self.delay = delay

		def func():
			while self.delay > 0:
				self.delay -= 1
				time.sleep(1)

				if self.delay <= 0:
					self.function()

		thread = threading.Thread(target=func)
		thread.start()
