import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fasio import start, spawn, sleep
from fasio.promise import Promise



async def set_val(p: Promise, i):
    print("Doing some heavy work in here")
    await sleep(1)
    p.set_value(f"2, {i}")
    print("Promise resolved")

    
async def main():
    st = []
    for i in range(5):
        p = Promise()
        spawn(set_val(p, i)) 
        st.append(p)

    for i in st:
        print(await i)


start(main())


