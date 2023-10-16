
from typing import Literal


class X7Cache(object):
    def __init__(self) :
        self._dev_broadcast_list = set([])
        self._dev_connected_list = set([])

    def broadcast_add(self, devno):
        self._dev_broadcast_list.add(devno)

    def broadcast_remove(self, devno):
        self._dev_broadcast_list.remove(devno)

    def connected_add(self, devno):
        self._dev_connected_list.add(devno)

    def connected_remove(self, devno):
        self._dev_connected_list.remove(devno)

    def get_broadcast_list(self):
        # 已连接的设备不再广播
        return self._dev_broadcast_list.difference(self._dev_connected_list)

    def clear(self, type : Literal['all', 'tcp', 'udp'] = 'udp'):

        if type == 'udp' or type == 'all' :
            self._dev_broadcast_list.clear()

        if type == 'tcp' or type == 'all' :
            self._dev_connected_list.clear()

# 全局对象
global_cache = X7Cache()


    


