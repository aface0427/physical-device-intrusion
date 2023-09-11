import threading


class MyThread(threading.Thread):
    """
     自带阻塞信号
    """

    def __init__(self, target=None, args=(), kwargs=None):
        self.event: threading.Event = threading.Event()  # 线程阻塞信号
        self.event.set()
        threading.Thread.__init__(self, target=target, args=args, kwargs=kwargs)


def ThreadFunc(funcName, *args, **kwargs):
    """
    把函数名封装成多线程,并开启进程
    :param funcName: 函数名
    :return: 返回线程对象
    """
    t = MyThread(target=funcName, args=args, kwargs=kwargs)
    t.setDaemon(True)
    t.start()
    # t.join()
    return t


def blockOtherThread():
    """
    阻塞除当前线程和主线程之外的所有线程
    :return:
    """
    aliveThread = threading.enumerate()
    print(aliveThread)
    for t in aliveThread:
        if t != threading.current_thread() and t != threading.main_thread():
            if hasattr(t, 'event'):
                print("Pause " + str(t))
                t.event.wait()
            if hasattr(t, 'finished'):
                print("Pause " + str(t))
                t.finished.set()


def notifyOtherThread():
    """
        唤醒除当前线程和主线程之外的所有线程
        :return:
        """
    aliveThread = threading.enumerate()
    print(aliveThread)
    for t in aliveThread:
        if t != threading.current_thread() and t != threading.main_thread() and hasattr(t, 'event'):
            print("Notify " + str(t))
            if hasattr(t, 'event'):
                print("Pause " + str(t))
                t.event.set()
            if hasattr(t, 'finished'):
                print("Pause " + str(t))
                t.finished.clear()
