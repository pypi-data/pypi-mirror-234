import ipdb
import random
import threading
import time

class myThread1(threading.Thread):
    def __init__(self, name=None, urls=None):
        if name:
            threading.Thread.__init__(self, name=name)
        else:
            print("请输入线程的名字。")
        self.urls = urls

    def run(self):
        print(f"Current {threading.current_thread().name} is running...")
        for url in self.urls:
                print(f"{threading.current_thread().name} ---->>> {url}")
                time.sleep(random.random())
        print(f"{threading.current_thread().name} ended.")

class myThread2(threading.Thread):
    def __init__(self, name=None):
        if name:
            threading.Thread.__init__(self, name=name)
        else:
            print("请输入线程的名字。")
            return
        if not hasattr(myThread2, "num"):
            myThread2.mylock = threading.RLock()
            myThread2.num = 0

    def run(self):
        # with myThread2.mylock:
        #     for i in range(5):
        #         print(f"{threading.current_thread().name} locked, Number: {self.num}")
        #         self.num += 1
        #         print(f"{threading.current_thread().name} released, Number: {self.num}")
        while True:
            myThread2.mylock.acquire()
            print(f"{threading.current_thread().name} locked, Number: {self.num}")
            if self.num >= 4:
                myThread2.mylock.release()
                print(f"{threading.current_thread().name} released, Number: {self.num}")
                self.num -= 1
                break
            myThread2.mylock.release()
            self.num += 1
            print(f"{threading.current_thread().name} released, Number: {self.num}")

def test_thread1():
	print(f"{threading.current_thread().name} is running...")
	t1 = myThread1(name='Thread_1',urls=['url_1','url_2','url_3'])
	t2 = myThread1(name='Thread_2',urls=['url_4','url_5','url_6'])
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print(f"{threading.current_thread().name} ended.")

def test_thread2():
    thread1 = myThread2('Thread_1')
    thread2 = myThread2('Thread_2')
    thread1.start()
    thread2.start()

if __name__ == '__main__':
	test_thread1()
	test_thread2()

'''test thread_lib'''
# import thread_lib

# thread_lib.test_thread1()
# thread_lib.test_thread2()
