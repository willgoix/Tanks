import threading, time

queue = []


def cancelAll():
    for funcs in queue:
        funcs.cancel()
    queue.clear()

class DelayedFunc:

    def __init__(self, function, delay):
        self.function = function
        self.delay = delay
        self.alive = True

        def func():
            while self.delay > 0 or self.alive:
                self.delay -= 1
                time.sleep(1)

                if self.delay <= 0:
                    self.function()

        thread = threading.Thread(target=func)
        thread.start()

        queue.append(self)

    def cancel(self):
        self.alive = False
