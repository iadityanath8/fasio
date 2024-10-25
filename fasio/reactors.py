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


# class Reactor:
    
#     def __init__(self, loop):
#         self._loop = loop
#         self.selector = selectors.DefaultSelector()
#         self._to_deregister = set()  # Track file descriptors to deregister after polling

#     def register_readers(self, fileno, task):
#         """Register the file descriptor for read events."""
#         if fileno in self._registered:
#             self.modify(fileno, selectors.EVENT_READ, task)
#         else:
#             self.selector.register(fileno, selectors.EVENT_READ, task)

#     def register_writers(self, fileno, task):
#         """Register the file descriptor for write events."""
#         if fileno in self._registered:
#             self.modify(fileno, selectors.EVENT_WRITE, task)
#         else:
#             self.selector.register(fileno, selectors.EVENT_WRITE, task)

#     def modify(self, fileno, events, task):
#         """Modify the registered events for the given file descriptor."""
#         self.selector.modify(fileno, events, task)

#     def __bool__(self):
#         return bool(self._registered)

#     def deregister(self, fileno):
#         """Deregister the file descriptor."""
#         if fileno in self._registered:
#             self.selector.unregister(fileno)

#     def poll(self, timeout):
#         """Poll for events and schedule tasks."""
#         events = self.selector.select(timeout)

#         for key, mask in events:
#             task = key.data
#             self._loop.call_soon(task)

#             # Mark the file descriptor for deregistration after all tasks are processed
#             self._to_deregister.add(key.fileobj)

#         # Deregister all marked file descriptors at once
#         for fileno in self._to_deregister:
#             self.deregister(fileno)
#         self._to_deregister.clear()  # Clear the set for the next poll cycle
            

class Reactor:
    
    def __init__(self, loop):
        self._loop = loop
        self.selector = selectors.DefaultSelector()
        self.tasks_to_deregister = []

    def register_readers(self, fileno, task):
        self.selector.register(fileno,selectors.EVENT_READ, task)

    def register_writers(self, fileno, task):
        self.selector.register(fileno, selectors.EVENT_WRITE, task)
    
    def __bool__(self):
        return bool(self.selector.get_map())

    def deregister(self, fileno):
        self.tasks_to_deregister.append(fileno)

    def poll(self, timeout):
        events = self.selector.select(timeout)

        for key, mask in events:
            task = key.data

            self._loop.call_soon(task)

            self.deregister(key.fileobj)

        # Perform batch deregistration after processing events
        for fileno in self.tasks_to_deregister:
            self.selector.unregister(fileno)
        self.tasks_to_deregister.clear()

__all__ = [" "]
