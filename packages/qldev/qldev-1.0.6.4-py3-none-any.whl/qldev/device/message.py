
from queue import Queue
from threading import Thread
from loguru import logger

from qldev.utils import crc16, get_ip


class UDPMessage(object):
    MessageStart = 'SHQuanLan'
    ConnectCommand = 0x10
    DeviceInfoCommand = 0x09

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_connect(devno, tcp_port=19128):
        message = bytearray(28)
        message[:10] = UDPMessage.MessageStart.encode('utf-8')
        cmd = UDPMessage.ConnectCommand
        devtype = 0x0
        
        # 本机ip
        ip = get_ip().split(".")
        
        message[10:12] = cmd.to_bytes(2, 'little')
        message[12:14] = devtype.to_bytes(2, 'little')
        #d57ee4dc99ce0940        
        message[14:22] = bytes.fromhex(devno)
        message[22] = (int)(ip[0])
        message[23] = (int)(ip[1])
        message[24] = (int)(ip[2])
        message[25] = (int)(ip[3])
        message[26:28] = tcp_port.to_bytes(2, 'little')
        checksum = crc16(message)

        return message + checksum.to_bytes(2, 'little')


class MessageChannel(Queue):
    def __init__(self, maxsize: int = ...) -> None:
        super().__init__(maxsize)
        self._run = True


    def subscribe(self, callback):
        consumer_thread = Thread(target=self.consumer, args=[callback])
        consumer_thread.start()

    def consumer(self, callback):
        while True:
            if self.qsize() > 0 or self._run:
                if callback:
                    callback(self.get())
                else:
                    self.get()

    def add(self, value):
        if self._run and value:
            self.put(value)
            
    def close(self):
        self._run = False

class X7MessageStream(object):
    def __init__(self) -> None:
        self.channels = {}

    def subscribe(self, key, maxsize = 1000, callback = None):
        if key is None:
            raise ValueError("Key is None")

        if key in self.channels.keys():
            logger.warning(f"Subscribe key {key} already exists.")

        # 每次订阅单独维护队列  
        self.channels[key] = MessageChannel(maxsize)
        self.channels[key].subscribe(callback)

    def remove(self, key):
        if self.channels[key]:
            self.channels[key].close()
            self.channels[key].remove(key)

    def _cache(self, packet):
        #将x7消息缓存到文件中
        return


    
