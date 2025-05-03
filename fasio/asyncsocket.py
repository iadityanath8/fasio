import _socket
from .eventloop import spawn, get_event_loop, kernel_switch

class socket:
    def __init__(self, family=_socket.AF_INET, sock_type=_socket.SOCK_STREAM, proto=0, fileno=None):
        self._sock = _socket.socket(family, sock_type, proto, fileno) if fileno is None else _socket.socket(fileno=fileno)
        self.__loop = get_event_loop()
        self._sock.setblocking(False)

    def bind(self, address):
        self._sock.bind(address)

    def listen(self, backlog=10):
        self._sock.listen(backlog)

    def setsockopt(self, level, optname, value):
        self._sock.setsockopt(level, optname, value)

    def getsockopt(self, level, optname):
        return self._sock.getsockopt(level, optname)

    def getsockname(self):
        return self._sock.getsockname()

    def getpeername(self):
        return self._sock.getpeername()

    def shutdown(self, how):
        self._sock.shutdown(how)

    def close(self):
        self._sock.close()

    async def recv(self, max_bytes=None, flags=0):
        while True:
            try:
                return self._sock.recv(max_bytes, flags)
            except BlockingIOError:
                self.__loop.read_wait(self._sock, self.__loop.current)
                self.__loop._EventLoop__current = None
                await kernel_switch()


    async def send(self, data, flags=0):
        while True:
            try:
                return self._sock.send(data, flags)
            except BlockingIOError:
                self.__loop.write_wait(self._sock, self.__loop.current)
                self.__loop._EventLoop__current = None
                await kernel_switch()

    async def sendto(self, data, address):
        while True:
            try:
                return self._sock.sendto(data, address)
            except BlockingIOError:
                self.__loop.write_wait(self._sock, self.__loop.current)
                await kernel_switch()

    async def sendall(self, data, flags=0):
        total_sent = 0
        while total_sent < len(data):
            sent = await self.send(data[total_sent:], flags)
            total_sent += sent

    async def accept(self):
        while True:
            try:
                client_sock_fd, addr = self._sock._accept()
                client = socket(fileno=client_sock_fd)
                client._sock.setblocking(False)
                return client, addr
            except BlockingIOError:
                self.__loop.read_wait(self._sock, self.__loop.current)
                self.__loop._EventLoop__current = None
                await kernel_switch()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()

__all__ = ['socket']
