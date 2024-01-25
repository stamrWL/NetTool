import socket
import sys
import threading

from .muxQueue import *
from .NetworkEnum import *
from .connection import connection
from .message import Message



class server_interface:
    def __init__(self,IPv4_Address = "192.168.3.37",Port = 60001) -> None:
        self.m_qMessagesIn = muxQueue()
        self.m_deqConnections = deque()
        self.m_asioAcceptor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.m_asioAcceptor.bind((IPv4_Address,Port))
        self.nIDCounter = 10000
        
        pass
    
    def Start(self)->bool:
        try:
            self.m_asioAcceptor.listen()
            self.waitThread = threading.Thread(target=self.WaitForClientConnection,)
            self.waitThread.start()

            pass
        except Exception as e:
            print(e)
            print("[SERVER] Exception")
            return False
        print("[SERVER] Started!")
        return True
        
    def Stop(self):
        pass
            
    def WaitForClientConnection(self):
        try:
            # print("start listen")
            socket_ , address_ = self.m_asioAcceptor.accept()
            print(f'[SERVER] New Connection: {address_} ')
            newconn = connection(socket_,self.m_qMessagesIn,owner.server)
            
            if self.OnClientConnect(newconn):
                self.m_deqConnections.append(newconn)
                newconn.ConnectToClient(self.nIDCounter)
                self.nIDCounter += 1
                print(f'[{newconn.GetID()}] Connection Approved')
            else:
                print(f'[{newconn.GetID()}] Connection Denied')
        except Exception as e:
            print(e)
            print("[SERVER] New Connection Error")
        self.waitThread = threading.Thread(target=self.WaitForClientConnection,)
        self.waitThread.start()
        pass
    
    def MessageClient(self,client:connection,message:Message):
        if client is not None and client.isConnnected():
            # print(f"[{client.GetID()}] has send ")
            self.SendTread = threading.Thread(target=client.Send , args=(message,))
            self.SendTread.start()
        else:
            self.OnClientDisconnect(client)
            self.m_deqConnections.remove(client)
            client = None
        pass
    
    def MessageAllClients(self,message:Message,pIgnoreClient:Message):
        bInvalidClientExists = False
        for client in self.m_deqConnections:
            if client is not None and client.isConnnected():
                if client is not pIgnoreClient:
                    self.SendTread = threading.Thread(target=client.Send , args=(message,))
                    self.SendTread.start()
            else:
                self.OnClientDisconnect(client)
                # self.m_deqConnections.remove(client)
                bInvalidClientExists = True
                client = None
    
        if bInvalidClientExists :
            # ?
            self.m_deqConnections.remove(None)
            
    def Update(self,nMaxMessages:int = -1):
        nMessageCount = 0
        if nMaxMessages is -1 :
            nMaxMessages = sys.maxsize
        while nMessageCount < nMaxMessages and not self.m_qMessagesIn.empty():
            msg = self.m_qMessagesIn.pop_front()
            # OnMess = threading.Thread(target=self.OnMessage,args=(msg[0],msg[1],))
            # OnMess.start()
            self.OnMessage(msg[0],msg[1])
            
            nMessageCount +=1
            
        pass
    
    def OnClientConnect(self,Client:connection)->bool:
        
        return True
    
    def OnClientDisconnect(self,Client:connection):
        pass
    
    def OnMessage(self,Client:connection,message:Message):
        pass