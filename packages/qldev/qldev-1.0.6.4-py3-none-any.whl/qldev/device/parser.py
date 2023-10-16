
from .message import UDPMessage
from qldev.utils import crc16


class MessageParser(object):
    def __init__(self) -> None:
        pass

class UDPParser(MessageParser):
    def __init__(self, channel = None) -> None:
        super().__init__()
        self._channel = channel

    def parse(self, packet, address):
        # print(f"receive udp message from {address[0]}:{address[1]}")
        plen = len(packet)
        # print(f"parse {packet} len {plen}")
        if plen < 10:
            return

        start = packet[:9].decode("utf-8")
        # quanlan udp message
        if start != UDPMessage.MessageStart:
            return

        if not check_crc(packet):
            print(f"数据CRC校验失败，丢弃！")
            return
        
        # message command
        cmd = int.from_bytes(packet[10:12], 'little')

        return self._parse(cmd, packet[12:])

    def _parse(self, cmd, data):
        # 只解析0x09
        if cmd == UDPMessage.DeviceInfoCommand:
            return self.parseDeviceInfo(data)
        else:
            # print(f'Ignore message which command is {hex(cmd)}')
            return None
        

    def parseDeviceInfo(self, data):
        # print(f"parseDeviceInfo {data}")
        devinfo = {}
        try:
            devinfo["dev_type"] = hex(int.from_bytes(data[:2], 'little'))
            devinfo["dev_id"] = data[2:10].hex()
            devinfo["version_code"] = int.from_bytes(data[42:46], 'little')
            devinfo["version_name"] = str(data[10:42],'utf-8').split('\x00')[0]
            if self._channel:
                self._channel.add(str(devinfo["dev_id"]))

        except Exception as e:
            print(f"parseDeviceInfo异常：{e}")

        # print(f"dev info is {devinfo}")
        return devinfo


def check_crc(data):
    return int.from_bytes(data[-2:], 'little')  == crc16(data[:-2])


