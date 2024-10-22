from eventloop import start, spawn , run_in_thread, sleep, run_in_process
import time 


def computer():
    print("AI TrAIn")
    time.sleep(1)
    print("COMPLETED AI TRAIN")

    return 1

async def runner():
    for _ in range(10):
        print("Hello world")
        await sleep(1)


async def main():
    v = run_in_process(computer)
    spawn(runner())
    
    print(await v)


start(main())
