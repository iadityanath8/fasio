from .eventloop import get_event_loop, Event, State


class Promise:

    def __init__(self):
        self.__value = None 
        self.__done = False
        self.__state = State.PENDING
        self._event = Event()
   
    def __await__(self):
        
        if self.__state == State.PENDING or self.__done == False:
            yield from self._event.__await__()
        
        return self.__value


    def __repr__(self):
        
        if self.__state == State.PENDING:
            return f"<Promise state={self.__state}>"

        elif self.__state == State.FINISHED:
            return f"<Promise state={self.__state} value={self.__value}>"
        else:
            return f"<Promise state={self.__state}>"

    def value(self):
        
        if self.__state == State.PENDING:
            raise Exception("Promise does not set right now")
        
        return self.__value

   
    def set_value(self, val):
        self.__value = val

        self._event.signal()




__all__ = ['Promise']