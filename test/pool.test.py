import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fasio import spawn, sleep, start
from fasio.promise import Promise
from fasio.eventloop import kernel_switch, Event
from fasio.queue import Queue

async def f():
    await sleep(3)
    print("Afetr")


async def g():
    await sleep(2)


async def main():
    # a = await 
    pass
## Optimize this more 
