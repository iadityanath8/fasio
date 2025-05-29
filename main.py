from fasio import start,run_in_thread, spawn
import time

def a():
    i =0
    for i in range(2): 
        time.sleep(1)        
        i += 1
    return i


async def do_print():
    for i in range(10):
        print(i)


async def main():
    p = run_in_thread(a)
    spawn(do_print())
    print(await p)


start(main())