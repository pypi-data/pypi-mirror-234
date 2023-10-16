
from .x7base import X7UDP, X7TCP

class X7Box(X7TCP):
    def __init__(self, tcp_port=19128, udp_port=54366, auto_search=False, callback=None):
        super().__init__(port=tcp_port, callback=callback)
        self._udp = X7UDP(port=udp_port, tcp_port=tcp_port, auto_search=auto_search)
    
    def connect(self, devno):
        self._udp.connect(devno=devno)
