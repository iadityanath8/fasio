from fasio import spawn, start, sleep, get_event_loop, kernel_switch, Queue

from collections import deque

class AsyncQueue:

    def __init__(self) -> None:
        self.items = deque()
        self.waiters = deque()
        self.loop = get_event_loop()

    async def get(self):
        if not self.items:
            self.waiters.append(self.loop._EventLoop__current)
            self.loop._EventLoop__current = None
            await kernel_switch()

        return self.items.popleft()

    def put(self, val):
        self.items.append(val)

        while self.waiters:
            self.loop.call_soon(self.waiters.popleft())



q = Queue()

async def runner():
    await sleep(1)
    q.put(1)
    await sleep(1)
    q.put(-1)
    q.put(12)
    q.put(1212)
"""
    user context switch kkab karna Blocking 

    whenever wait thereever await
"""


async def cosumer():
    for i in range(10):
        print(await q.get())

async def producer():
    for i in range(10):
        q.put(i)
        await sleep(2)


async def main():
    spawn(cosumer())
    # print(await q.get())
    # print(await q.get())
    spawn(producer())

# spawn(runner()) 
start(main())