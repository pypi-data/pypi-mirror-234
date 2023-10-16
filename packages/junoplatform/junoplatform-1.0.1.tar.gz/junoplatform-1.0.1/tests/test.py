from threading import Thread, Lock

import time


class A:
    pass


class B(object):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._lock.acquire()
            if not cls._instance:
                # simulate time consumming constructs
                time.sleep(0)
                cls._instance = super().__new__(cls)
            cls._lock.release()

        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        print(self)

# test singleton pattern


def f1():
    B(1)


def f2():
    B(2)


th1 = Thread(target=f1)
th1.start()

th2 = Thread(target=f2)
th2.start()

time.sleep(10)
