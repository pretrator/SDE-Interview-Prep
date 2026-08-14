import threading
import time

class BadCounter():
    def __init__(self):
        self.threads = []
        self.counter = 0

    def counter1(self):
        for _ in range(1000):
            self.counter += 1
            

    def addThreads(self, th):
        self.threads.append(th)

    def startThreads(self):
        for th in self.threads:
            th.start()

    def wait(self):
        for th in self.threads:
            th.join()

    def createThreads(self, threadNumber):
        for _ in range(threadNumber):
            self.addThreads(threading.Thread(target=self.counter1))

    def testCounter(self):
        self.createThreads(100)

        self.startThreads()
        self.wait()

        print(self.counter)

bdc = BadCounter()
bdc.testCounter()