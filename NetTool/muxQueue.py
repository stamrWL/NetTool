from collections import deque
import threading

class muxQueue:
    # 这是一个只允许单一访问的双向队列
    # 可能死锁！！
    def __init__(self) -> None:
        self.Queue = deque()
        self.Lock = threading.Lock()
        pass

    def front(self):
        self.Lock.acquire()
        while len(self.Queue) is 0:
            self.Lock.release()
            self.Lock.acquire()
            
        front = self.Queue[0]
        self.Lock.release()
        return front
    
    def back(self):
        self.Lock.acquire()
        while len(self.Queue) is 0:
            self.Lock.release()
            self.Lock.acquire()
        
        back = self.Queue[-1]
        self.Lock.release()
        return back
    
    def pop_front(self):
        self.Lock.acquire()
        while len(self.Queue) is 0:
            self.Lock.release()
            self.Lock.acquire()
        front = self.Queue[0]
        self.Queue.popleft()
        self.Lock.release()
        return front

    def pop_back(self):
        self.Lock.acquire()
        while len(self.Queue) is 0:
            self.Lock.release()
            self.Lock.acquire()
        back = self.Queue[-1]
        self.Queue.pop()
        self.Lock.release()
        return back
    
    def push_front(self,value):
        self.Lock.acquire()
        self.Queue.appendleft(value)
        self.Lock.release()
        
    def push_back(self,value):
        self.Lock.acquire()
        self.Queue.append(value)
        self.Lock.release()
        
    def empty(self)->bool:
        self.Lock.acquire()
        is_empty = len(self.Queue) is 0
        self.Lock.release()
        return is_empty 
    
    def clear(self):
        self.Lock.acquire()
        self.Queue.clear()
        self.Lock.release()
    
    def count(self):
        self.Lock.acquire()
        count = len(self.Queue)
        self.Lock.release()
        return count
    
    def __del__(self):
        self.Queue.clear()
        