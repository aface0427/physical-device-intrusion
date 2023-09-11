import threading
from threading import Timer


class TimerUtil:
    def __init__(self, interval, function_name, *args, **kwargs):
        """
        :param interval:时间间隔
        :param function_name:可调用的对象
        :param args:args和kwargs作为function_name的参数
        """
        self.timer = RepeatingTimer(interval, function_name, *args, **kwargs)
        self.timer.setDaemon(True)

    def timer_start(self):
        self.timer.start()

    def timer_cancle(self):
        self.timer.cancel()


class RepeatingTimer(Timer):
    def __init__(self,interval, function, args=None, kwargs=None):
        super().__init__(interval, function, args, kwargs)

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
