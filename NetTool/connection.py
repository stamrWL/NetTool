import socket
import threading

from .NetworkEnum import *
from .message import Message,MessageHeader
from .muxQueue import muxQueue

class connection:
    # 用于表示一个用于连接的对象，在server端表示的是用户，在user端表述的是服务器
    def __init__(self,socket:socket,m_qMessagesIn:muxQueue,owner : owner) -> None:
        # socket的是监听到的连接用户(换一个端口进行通讯，不占用lisen端口)，m_qMessagesIn是消息写入队列(整个程序只有一个消息接收队列)
        self.socket = socket
        self.m_qMessagesIn = m_qMessagesIn
        self.m_qMessagesOut = muxQueue()
        self.m_nOwnerType = owner
        
        self.id = 0
       
        pass
    
    def __WriteHeader(self):
        try:
            self.socket.send(self.m_qMessagesOut.front().pack_head())
            if self.m_qMessagesOut.front().BodySize() > 0:
                self.__WriteBody()
            else:
                self.m_qMessagesOut.pop_front()
                if not self.m_qMessagesOut.empty():
                    self.__WriteHeader()
        except Exception as e:
            print(e)
            self.Disconnect()
            print(f"[{self.id}] Write Header Fail.")
        pass
    
    def __WriteBody(self):
        try:
            self.socket.send(self.m_qMessagesOut.front().pack_body())
            self.m_qMessagesOut.pop_front()
            if not self.m_qMessagesOut.empty():
                self.__WriteHeader()
            pass
        except Exception as e:
            print(e)
            self.Disconnect()
            print(f"[{self.id}] Write Body Fail.")
            
    def __AddToIncomingMessageQueue(self,msg:Message):
        if self.m_nOwnerType == owner.server:
            self.m_qMessagesIn.push_back((self,msg))
        else:
            self.m_qMessagesIn.push_back((None,msg))
            
        self.ReadThread = threading.Thread(target=self.__ReadHeader ) 
        self.ReadThread.start()
        pass  
        
    def __ReadHeader(self):
        try:
            data = self.socket.recv(MessageHeader.GetSize())
            msg = Message()
            header = msg.header
            header.unpack(data)
            if msg.header.BodySize > 0:
                self.__ReadBody(msg)
            else:
                self.__AddToIncomingMessageQueue(msg)
            pass
        except Exception as e:
            print(e)
            print(f"[{self.id}] Read Header Fail")
            pass
    
    def __ReadBody(self,msg:Message):
        try:
            data = self.socket.recv(msg.header.BodySize)
            msg.input_bytearray(data)
            self.__AddToIncomingMessageQueue(msg)
            pass
        except Exception as e:
            print(e)
            print(f"[{self.id}] Read Body Fail")
            pass
        pass
    
    def GetID(self):
        return self.id
    
    def ConnectToClient(self,uid = 0):
        if self.m_nOwnerType == owner.server:
            if self.socket._closed == False:
                self.id = uid
                self.ReadThread = threading.Thread(target=self.__ReadHeader ) 
                self.ReadThread.start()
            pass
        
    def Disconnect(self):
        self.socket.close()
        
    def isConnnected(self)->bool:
        return not self.socket._closed
    
    def StartListening(self):
        pass
    
    def Send(self,msg:Message):
        bWritingMessage = not self.m_qMessagesOut.empty()
        self.m_qMessagesOut.push_back(msg)
        if not bWritingMessage:
            self.__WriteHeader()
            pass