import select
import selectors 

class BaseSelectReactor:

    def __init__(self, loop):

        self.__readwaiters  = {  }
        self.__writewaiters = {  }
        self._loop = loop
    
    def __bool__(self):
        if self.__readwaiters or self.__writewaiters:
            return True

        return False 

    def register_readers(self,fileno, task):
        self.__readwaiters[fileno] = task


    def register_writers(self, fileno, task):
        self.__writewaiters[fileno] = task


    def poll(self,timeout):
        can_read, can_write, [] = select.select(self.__readwaiters, self.__writewaiters,[], timeout)

        for rfd in can_read:
            self._loop.call_soon(self.__readwaiters.pop(rfd))

        for wfd in can_write:
            self._loop.call_soon(self.__writewaiters.pop(wfd))



class Reactor:
    
    def __init__(self, loop):
        self._loop = loop
        self.selector = selectors.DefaultSelector()

    def register_readers(self, fileno, task):
        self.selector.register(fileno,selectors.EVENT_READ, task)

    def register_writers(self, fileno, task):
        self.selector.register(fileno, selectors.EVENT_WRITE, task)
    
    def __bool__(self):
        return bool(self.selector.get_map())

    def deregister(self, fileno):
        self.selector.unregister(fileno)

    def poll(self, timeout):
        events = self.selector.select(timeout)

        for key, mask in events:
            task = key.data

            self._loop.call_soon(task)

            self.deregister(key.fileobj)




