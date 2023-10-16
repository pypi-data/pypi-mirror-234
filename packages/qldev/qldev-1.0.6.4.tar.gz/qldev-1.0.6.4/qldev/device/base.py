from ctypes.wintypes import HICON
import struct

def bytes_to_float(ba):
    return struct.unpack('f', ba)[0]

def bytes_to_number(bs, isBig=True):
    return int.from_bytes(bs, byteorder='little', signed=isBig)

def to_long(bs, isBig=True):
    return int.from_bytes(bs, byteorder='little', signed=isBig)

class Message(object):
    def __init__(self) -> None:
        pass

    def parse(packet) -> None:
        pass


