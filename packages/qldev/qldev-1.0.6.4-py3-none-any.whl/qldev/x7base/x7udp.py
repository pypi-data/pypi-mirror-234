from threading import Thread
from time import sleep
from qldev.device import UDPParser, MessageChannel, UDPMessage
from qldev.network import UDPReceiver, UDPSender
from .x7parser import *
from .devinfo import *

class X7UDP(object):
    def __init__(self, port = 54366, tcp_port=19128, auto_search = False, broadcast_interval = 3) :
        self._port = port
        self._sender = None
        self._receiver = None
        self._tcp_port = tcp_port
        self._list = []
        self._broadcast_interval = broadcast_interval
        self._create_server()
        if auto_search :
            self._create_client()

    # udp服务端
    def _create_server(self):
        if self._sender:
            return
        
        self._sender = UDPSender(port=self._port)
        # connect消息发送
        notify_thread = Thread(target=self._connect)
        notify_thread.start()

    # udp客户端
    def _create_client(self):
        if self._receiver:
            return
        
        channel = MessageChannel(maxsize=100)
        channel.subscribe(self.connect)
        parser = UDPParser(channel)
        
        self._receiver = UDPReceiver(parser=parser, port=self._port)
        # 消息监听
        client_thread = Thread(target=self._receiver.accept)
        client_thread.start()

    # 通过广播通知设备连接服务端
    def connect(self, devno):
        global_cache.broadcast_add(devno)

    
    # 发送广播
    def _connect(self):
        while True:
            list = global_cache.get_broadcast_list()
            for idx, item in enumerate(list):
                logger.info(f"search for device({item}).")
                message = UDPMessage.get_connect(item, self._tcp_port)            
                self._sender.send(message=message)

            # 广播间歇
            if self._broadcast_interval >  0:
                sleep(self._broadcast_interval)
    
    # 开启客户端
    def open_client(self):
        self._create_client()

    # 清空广播列表
    def clear_broadcast(self, type: Literal['all', 'tcp', 'udp'] = 'udp'):
        global_cache.clear(type)

    def close(self):
        if self._sender:
            self._sender.close()

        if self._receiver:
            self._receiver.close()