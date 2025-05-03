from fasio import spawn, start, sleep, gather, collect


async def f():
    await sleep(1)
    print("Billu has")
    return 1

async def g():
    print("Meow Meow")
    return 2

async def p():
    for _ in range(3):
        await sleep(0.4)
    return 12

async def main():   
    c = await collect(f(),g(),p())
    print(c)

start(main())