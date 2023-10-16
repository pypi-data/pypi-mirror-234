from cmath import log
from ipaddress import ip_address
from socket import *
from time import strftime
from loguru import logger

class UDPSender(object):
    def __init__(self, ip = "255.255.255.255", port = 54366) :
        self._address = (ip, port)
        self._socket = None
        self.socket()
    
    def socket(self):
        if self._socket is None:
            self._socket = socket(AF_INET, SOCK_DGRAM)
            self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        return self._socket
        
    def send(self, message):
        try:
            self._socket.sendto(message, self._address)
        except Exception as e:
            logger.error("Exception on UDPSender send.")
            logger.error(e)
    
    def close(self):
        if self._socket :
            self._close()


class UDPReceiver(object):
    def __init__(self, parser=None, channel=None, port=54366):
        self._run = False
        self._port = port
        self._socket = None
        self._parser = parser
        self._channel = channel

    def close(self):
        self._run = False

    def accept(self):
        if self._port is None:
            logger.error(f"UDPReceiver未设置监听端口！")
            return

        if self._run:
            logger.warning(f"UDPReceiver正在监听端口{self._port}, 本次操作已忽略。")
            return

        self._run = True
        if self._socket is None:
            self._socket = socket(AF_INET, SOCK_DGRAM)  
            self._socket.bind(('', self._port)) 

        while self._run:
            # print(f"等待从端口{self._port}获取数据...")
            udp_data = self._socket.recvfrom(1024) 
            self._parser.parse(udp_data[0], udp_data[1])
            
        logger.info(f"关闭端口{self._port}的连接")
        self._close()  #关闭套接字
    
    def add_connect(self, devinfo):
        print(devinfo)
        if self._channel and devinfo:
            self._channel.put(devinfo['dev_id'])
