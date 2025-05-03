import asyncio

HOST = "0.0.0.0"
PORT = 8888

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    # print(f"Connection from {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break  # Client closed connection
            writer.write(data)  # Echo back
            await writer.drain()  # Flush data
    except asyncio.CancelledError:
        pass  # Handle cancellation cleanly
    finally:
        writer.close()
        await writer.wait_closed()
        # print(f"Closed connection: {addr}")

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    # print(f"Asyncio Echo Server listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
