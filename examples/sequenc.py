import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fasio import spawn, start, sleep, socket

async def main():
    server = socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(('localhost',3000))
    server.listen(socket.SOMAXCONN)

    while True:
        client, addr = await server.accept()

        spawn(handle_client(client))


async def handle_client(client):
    while True:
        data = await client.recv(111)
        if not data:
            client.close()
            break
    
        await client.send(data)


start(main())