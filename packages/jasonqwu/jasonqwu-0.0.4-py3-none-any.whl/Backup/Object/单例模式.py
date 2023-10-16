import threading
import time

class Singleton:
    instance = None
    lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        with cls.lock:
            if cls.instance:
                return cls.instance
            time.sleep(0.1)
            cls.instance = super().__new__(cls)
            return cls.instance

    def __init__(self, name=None):
        self.name = name

def task():
    obj = Singleton("xxx")
    print(obj)

def main():
    for i in range(10):
        t = threading.Thread(target=task)
        t.start()

    obj1 = Singleton("Alex")
    print(obj1)
    obj2 = Singleton("Jason")
    print(obj2)

if __name__ == '__main__':
    main()
