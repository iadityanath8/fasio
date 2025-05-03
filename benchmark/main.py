
import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from fasio import spawn, start
from fasio.asyncsocket import socket

async def handle_client(client):
    try:
        while True:
            data = await client.recv(1024)
            if not data:
                break
            await client.sendall(data)
    finally:
        client.close()

async def echo_server(host='127.0.0.1', port=8888):
    server = socket()
    server.bind((host, port))
    server.listen()
    # print(f"Echo server listening on {host}:{port}")
    
    while True:
        client, addr = await server.accept()
        # print(f"Connection from {addr}")
        spawn(handle_client(client))


start(echo_server())
