import threading


class RepeatingTimer(threading.Timer):
    def __init__(self, interval, function):
        super(RepeatingTimer, self).__init__(interval, function)

    def run(self) -> None:
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
