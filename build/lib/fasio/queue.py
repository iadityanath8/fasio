from .eventloop import Event
import heapq
from collections import deque

"""
    get, put , __repr__, ___bool__ , empty, get_sync, put_sync 
    pop, push, ""          ""        ""      push_sync, pop_sync 
"""


class QueueEmptyException(Exception):
    """Raised when attempting to retrieve an item from an empty queue."""
    def __init__(self, message="Queue is empty and no items are available to retrieve."):
        super().__init__(message)



class Queue:
    def __init__(self) -> None:
        self.items = deque()
        self._event = Event()
    
    def __repr__(self) -> str:
        return f"<Queue state={self._event.state}> at {hex(id(self))}"

    def __bool__(self):
        return bool(self.items)
        
    def get_sync(self):
        if not self.items:
            raise QueueEmptyException()

    
    async def get(self):
        if not self.items:
            await self._event.wait()    # if empty then pause 
            
        return self.items.popleft()
    
    def put_sync(self, val):
        self.items.append(val)


    def put(self,val):
        self.items.append(val)        
        self._event.signal()     # if some item resume pause 


class Deque:
    def __init__(self) -> None:
        self.items = deque()
        self._event = Event()
    
    def __repr__(self) -> str:
        return f"<Dqueue state={self._event.state}> at {hex(id(self))}"
    
    def __bool__(self):
        return bool(self.items)
        
    def get_sync_left(self):
        if not self.items:
            raise QueueEmptyException()
        
        return self.items.popleft()
    
    def get_sync_right(self):
        if not self.items:
            raise QueueEmptyException()
        
        return self.items.pop()

    async def get_left(self):
        if not self.items:
            await self._event.wait()
        
        return self.items.popleft()
    
    async def get_right(self):
        if not self.items:
            await self._event.wait()
        
        return self.items.pop()
    
    def put_sync_left(self, val):
        self.items.appendleft(val)

    def put_sync_right(self, val):
        self.items.append(val)
    
    def put_left(self, val):
        self.items.appendleft(val)
        self._event.signal()

    def put_right(self, val):
        self.items.append(val)
        self._event.signal()


class Heap:
    def __init__(self) -> None:
        self.items = []
        self._event = Event()

    def __repr__(self) -> str:
        return f"<HeapQueue state-{self._event.state}> at {hex(id(self))}"
    
    def __bool__(self):
        if len(self.items) > 0:
            return True
        else:
            False
    
    def get_sync(self):
        return heapq.heappop(self.items)

    async def get(self):
        if len(self.items) == 0:
            await self._event.wait()

        return heapq.heappop(self.items)
    
    def peek(self):
        return self.items[0]

    def put_sync(self, val):
        heapq.heappush(self.items, val)

    def put(self, val):
        heapq.heappush(self.items, val)
        self._event.signal()


__all__ = ['Queue', 'Heap', 'Deque']
