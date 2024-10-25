import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fasio import spawn, start, sleep, socket, Queue



async def consumer(q):
    for _ in range(10):
        print(await q.get())


async def producer(q):
    for i in range(10):
        q.put(i)
        await sleep(1)



async def main():
    q = Queue()
    spawn(producer(q))
    spawn(consumer(q))


start(main())