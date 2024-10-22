import _socket
from eventloop import get_event_loop, kernel_switch



class socket(_socket.socket):
    
    AF_INET      = _socket.AF_INET
    SO_REUSEADDR = _socket.SO_REUSEADDR
    SOCK_STREAM  = _socket.SOCK_STREAM
    SOL_SOCKET   = _socket.SOL_SOCKET
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__loop = get_event_loop()

    
    async def recv(self,max_bytes=1024, flags=0):
        self.__loop.read_wait(self, self.__loop.current)
        self.__loop._EventLoop__current = None 
        await kernel_switch()
        return super().recv(max_bytes, flags)

    async def send(self,data, flags=0):
        self.__loop.write_wait(self, self.__loop.current)
        self.__loop._EventLoop__current = None 
        await kernel_switch()
        return super().send(data, flags)


    async def accept(self):
        self.__loop.read_wait(self, self.__loop.current)
        self.__loop._EventLoop__current = None 
        await kernel_switch()
        fd, addr = super()._accept()
        return socket(fileno=fd), addr

    def getpeername(self):
        return super().getpeername()


    def getsockname(self):
        return super().getsockname()


    def listen(self, max_val=4):
        return super().listen(max_val)


    def bind(self, addr):
        return super().bind(addr)




