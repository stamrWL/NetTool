import struct
import ctypes
from enum import Enum

class MessageHeader(ctypes.Structure):
    _fields_ = [
        ('id',ctypes.c_uint32),
        ('thread_id',ctypes.c_uint32),
        ('BodySize',ctypes.c_uint32),
    ]
    
    format = 'III'
    
    def __init__(self, message_id = 0, thread_id = -1):
        self.id = message_id
        self.thread_id = thread_id
        self.BodySize = 0
    
    @staticmethod
    def GetSize():
        return struct.calcsize(MessageHeader.format)

    def pack(self):
        # Pack the header data into bytes
        return bytearray(self)

    def unpack(self, data):
        # Unpack the header data from bytes
        unpacked_data = struct.unpack(self.format, data)
        self.id, self.thread_id, self.BodySize = unpacked_data

        
        
class Message:
    def __init__(self, message_id = 0, thread_id = -1):
        # Message的初始化，message_id是用于表述消息类型，thread_id是用户端的消息(是用户第几个线程发出的消息)，不知道就用-1
        if issubclass(type(message_id),Enum):
            message_id = message_id.value
        self.header = MessageHeader(message_id,thread_id)
        self.body = bytearray()

    def __str__(self) -> str:
        return f"ID: {self.header.id} Thread_id: {self.header.thread_id} Size: {self.header.BodySize}"
    
    def BodySize(self) -> int:
        # 获取信息长度
        return len(self.body)

    def set_data(self,data) -> None:
        # 设置body为二进制对象
        self.body = bytearray(data)
    
    def input_fmt(self, fmt: str, data) -> None:
        # Pack the data into bytes and extend the bytearray
        self.body.extend(struct.pack(fmt, data))
        
        # Recalculate the message size
        self.header.BodySize = self.BodySize()
        
    def input_bytearray(self,data):
        self.body.extend(data)
        
        self.header.BodySize = self.BodySize()
        
    def input_string(self,string : str):
        string = string.encode('utf-8')
        CtypeString = ctypes.create_string_buffer(string)
        self.input_bytearray(CtypeString)
        stringLen = ctypes.sizeof(CtypeString)
        self.input_bytearray(ctypes.c_int32(stringLen))

    def output_fmt(self, fmt: str):
        # 将body队尾的二进制文件用fmt的格式进行读取，并删除
        # Cache the location towards the end of the bytearray where the pulled data starts
        i = len(self.body) - struct.calcsize(fmt)
        
        # Unpack the data from the bytearray
        unpacked_data = struct.unpack_from(fmt, self.body, i)
        
        # Shrink the bytearray to remove read bytes
        self.body = self.body[:i]
        
        # Recalculate the message size
        self.header.BodySize = self.BodySize()
        
        return unpacked_data
    
    def output_c_type(self, type: ctypes._SimpleCData):
        length = ctypes.sizeof(type)
        # Cache the location towards the end of the bytearray where the pulled data starts
        i = len(self.body) - length
        
        # Unpack the data from the bytearray
        unpacked_data = type.from_buffer(self.body[i:])
        
        # Shrink the bytearray to remove read bytes
        self.body = self.body[:i]
        
        # Recalculate the message size
        self.header.BodySize = self.BodySize()
        
        return unpacked_data
    
    def output_string(self):
        stringLen = self.output_c_type(ctypes.c_int32).value
        
        i = len(self.body) - stringLen

        # Unpack the data from the bytearray
        unpacked_data = self.body[i:].decode('utf-8')
        
        # Shrink the bytearray to remove read bytes
        self.body = self.body[:i]

        # Recalculate the message size
        self.header.BodySize = self.BodySize()

        return unpacked_data.replace('\x00','')
    
    def pack_head(self):
        # 把头打包
        return self.header.pack()
    
    def pack_body(self):
        return self.body