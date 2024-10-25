import _socket
from .eventloop import spawn, get_event_loop, kernel_switch


"""  Just a prototypal socket stil most of the works remain the class and object creation and inheritance is overhead in here """
"""  We will soon make our socket class which will be productionally functional and fast """


"""

    !!! We Recommend u not to use this as of now in any production application because this is still in development !!!

"""
class socket(_socket.socket):

    # Define socket constants as class attributes

    AF_INET = _socket.AF_INET
    AF_INET6 = _socket.AF_INET6
    AF_UNIX = _socket.AF_UNIX
    SOCK_STREAM = _socket.SOCK_STREAM
    SOCK_DGRAM = _socket.SOCK_DGRAM
    SOCK_RAW = _socket.SOCK_RAW
    SOCK_SEQPACKET = _socket.SOCK_SEQPACKET
    SOCK_RDM = _socket.SOCK_RDM
    SOCK_NONBLOCK = _socket.SOCK_NONBLOCK
    SOCK_CLOEXEC = _socket.SOCK_CLOEXEC
    SO_REUSEADDR = _socket.SO_REUSEADDR
    SO_KEEPALIVE = _socket.SO_KEEPALIVE
    SO_BROADCAST = _socket.SO_BROADCAST
    SO_LINGER = _socket.SO_LINGER
    SO_OOBINLINE = _socket.SO_OOBINLINE
    SO_SNDBUF = _socket.SO_SNDBUF
    SO_RCVBUF = _socket.SO_RCVBUF
    SO_SNDTIMEO = _socket.SO_SNDTIMEO
    SO_RCVTIMEO = _socket.SO_RCVTIMEO
    SO_ERROR = _socket.SO_ERROR
    SOL_SOCKET = _socket.SOL_SOCKET
    IPPROTO_TCP = _socket.IPPROTO_TCP
    IPPROTO_UDP = _socket.IPPROTO_UDP
    SOMAXCONN = _socket.SOMAXCONN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__loop = get_event_loop()
        self.setblocking(False)

    def bind(self, address):
        """
             Direct override no need required to use asynchronous programming
             because of the NON BLOCKING NATURE
        """
        super().bind(address)

    def listen(self, backlog=10):
        """
            Direct override no need required to use asynchronous programming
            because of the NON BLOCKING NATURE
        """
        super().listen(backlog)

    async def recv(self, max_bytes=None, flags=0):
        self.__loop.read_wait(self, self.__loop.current)
        self.__loop._EventLoop__current = None
        await kernel_switch()

        return super().recv(max_bytes)

    async def send(self, data, flags=0):
        while True:
            try:
                return super().send(data, flags)
            except BlockingIOError:    
                self.__loop.write_wait(self, self.__loop.current)
                self.__loop._EventLoop__current = None
                await kernel_switch()

    async def sendto(self, data, address):
        while True:
            try:
                return super().sendto(data, address)
            except BlockingIOError:
                self.__loop.write_wait(self, self.__loop.current)
                await kernel_switch()

    def getpeername(self):
        return super().getpeername()

    def getsockname(self):
        return super().getsockname()

    def shutdown(self, how):
        return super().shutdown(how)

    async def sendall(self, data, flags = 0):
        total_send = 0
        while total_send < len(data):
            sent = await self.send(data[total_send:],flags)
            total_send += sent

    async def accept(self):

        while True:
            try:
                client_sock_fd, addr = super()._accept()
                client = socket(fileno=client_sock_fd)           # SOON WOOW GOOD SO MUCH NON BLOCKING WOOW 
                client.setblocking(False)
                return client, addr
            except BlockingIOError:
                # print("Blockin io ")
                self.__loop.read_wait(self, self.__loop.current)
                self.__loop._EventLoop__current = None
                await kernel_switch()


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()




__all__ = ['socket']
