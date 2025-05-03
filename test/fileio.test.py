import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fasio import start, spawn, run_in_thread, sleep
import time

CHUNK_SIZE = 12  

def blocking_file_reader(filename):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break  

            time.sleep(1)
            yield chunk


async def async_file_reader(filename):
    for chunk in await run_in_thread(blocking_file_reader, filename):
        print("Read chunk:", chunk.decode(errors="ignore"))


async def print_message():
    for i in range(10):
        print(f"Doing other work... {i}")
        await sleep(1)


async def main():
    filename = "large_file.txt"
    spawn(print_message())
    spawn(async_file_reader(filename))  # Spawn async file reader
    spawn(async_file_reader(filename))

start(main())  # Start Fasio event loop
