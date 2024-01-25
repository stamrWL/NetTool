import socket
import sys
import threading

from .muxQueue import muxQueue
from .NetworkEnum import *
from .connection import connection
from .message import Message

class client_interface:
    def __init__(self) -> None:
        self.m_connection = None
        self.sock = None
        self.m_qMessagesIn = muxQueue()
        pass
    
    def IsConnected(self) -> bool:
        if self.m_connection is not None:
            return self.m_connection.isConnnected()
        else:
            return False
    
    def Connect(self,host:str ,port:int):
        sock = None
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((host,port))
            self.m_connection = connection(sock,self.m_qMessagesIn,owner.client)
        except Exception as e:
            print(e)
            print("[Client] Exception")
        
    def Disconnect(self):
        if self.IsConnected():
            self.m_connection.Disconnect()
        self.m_connection = None
        
    def Send(self,msg:Message):
        if self.IsConnected():
            self.m_connection.Send(msg)
            
    def Incoming(self)->muxQueue:
        return self.m_qMessagesIn