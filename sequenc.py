import time
from collections import deque

class Scheduler:
    def __init__(self):
        self.ready = deque()

    def call_soon(self, func):
        self.ready.append(func)

    def run(self):
        while self.ready:
            func = self.ready.popleft()
            func()

sche = Scheduler()

def printMeow(n):
    if n > 0:
        print("MEow", n)
        time.sleep(1)
        sche.call_soon(lambda: printMeow(n - 1))

def printBruh(s, x = 0):
    if x < s:
        print("Yo", x)
        time.sleep(1)
        sche.call_soon(lambda: printBruh(s, x + 1))

sche.call_soon(lambda: printMeow(3))
sche.call_soon(lambda: printBruh(3))
sche.run()

#sequential exec
#printMeow(3)
#printBruh(3)


#concurrent execution
#way is to use threads

#import threading

#threading.Thread(target=printMeow, args=(3,)).start()
#threading.Thread(target=printBruh, args=(3,)).start()
