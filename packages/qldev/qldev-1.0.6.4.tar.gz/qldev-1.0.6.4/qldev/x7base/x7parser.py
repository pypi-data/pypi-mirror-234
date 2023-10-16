
from struct import pack
from loguru import logger


from .x7utils import CommandEnum
from qldev.utils import crc16, get_ip


class MessageParser(object):
    def __init__(self) -> None:
        pass

    def parse(self, packet, callback = None):
        # print(f"MessageParser.parse. packet is {packet}")
        plen = len(packet)
        if plen < 10:
            logger.warning(f"MessageParser.parse. Not support message len: {len}")
            return
        
        cmd = int.from_bytes(packet[12:14], 'little')
        
        result = self.parse_by_cmd(cmd, packet[14:-2])
        if callback:
            callback(cmd, result)

    def parse_by_cmd(self, cmd, data):
        # 结果校验
        result = (int)(data[8])
        if result != 0:
            logger.warning(f"cmd {hex(cmd)} result is {result}")
            return None

        if cmd == CommandEnum.GET_DEVICE_INFO:
            return self.get_device_info(data)
            
        if cmd == CommandEnum.SIGNALS:
            return self.signals(data)
            
        if cmd == CommandEnum.TRIGGER:
            return self.trigger(data)
            
        if cmd == CommandEnum.WAV_UPDATE_READY:
            return self.wav_update_ready(data)
            
        if cmd == CommandEnum.WAV_UPDATE:
            return self.wav_update(data)
            
        if cmd == CommandEnum.WAV_UPDATE_STOP:
            return self.wav_update_stop(data)
            
        if cmd == CommandEnum.WAV_TRIGGER:
            return self.wav_trigger(data)

        return self.not_support(cmd, data)
        

    def get_device_info(self, data):
        info = {}
        info["dev_id"] = data[9:17].hex()
        info["dev_type"] = int.from_bytes(data[17:21], 'little')
        info["sw_version"] = int.from_bytes(data[21:25], 'little')
        info["hw_version"] = int.from_bytes(data[25:29], 'little')
        logger.debug(f"get_device_info->{info}")
        return info

    def signals(self, data):
        logger.debug(f"packet len is {len(data)}")
        packet = {}
        packet["packet_id"] = int.from_bytes(data[9:17], 'little')
        packet["channels"] = data[17:49]
        # packet["origin_rate"] = int.from_bytes(data[45:49], 'little')
        packet["origin_rate"] = int.from_bytes(data[49:53], 'little')
        packet["sample_rate"] = int.from_bytes(data[53:57], 'little')
        packet["sample_len"] = int.from_bytes(data[57:61], 'little')
        packet["resolution"] = int.from_bytes(data[61:63], 'little')
        packet["filter"] = int(data[63])
        packet["data_len"] = int.from_bytes(data[64:68], 'little')
        packet["data"] = data[68:]

        return packet
        
    def trigger(self, data):
        logger.debug("trigger success.")
        return
        
    def wav_update_ready(self, data):
        logger.debug("wav_update_ready success.")
        return
        
    def wav_update(self, data):
        logger.debug("wav_update success.")
        return
        
    def wav_update_stop(self, data):
        logger.debug("wav_update_stop success.")
        return
        
    def wav_trigger(self, data):
        logger.debug("wav_trigger success.")
        return
        
    def not_support(self, cmd, data):
        logger.warning(f"cmd({cmd})not support.")
        return

        
class X7Parser(object):
    UDP_START = "SHQuanLan"
    NOTIFY_CMD = 0x10
    INFO_CMD = 0x09

    def __init__(self) -> None:
        self._base = None
        self._message = None

    def parse(self, packet):
        plen = len(packet)
        if plen < 10:
            return

        start = packet[:9].decode("utf-8")
        # quanlan udp message
        if start != X7Parser.UDP_START:
            logger.warning(f"unexcept message header.")
            return

        if not check_crc(packet):
            print(f"CRC verification failed!")
            return

        self._message = None
        cmd = int.from_bytes(packet[10:11], 'little')

        if cmd == 0x10:
            logger.debug(parse_net_param(packet[12:-2]))

        if cmd == 0x09:
            logger.debug(parse_net_param(packet[12:-2]))

    #devno是hex字符串
    @staticmethod
    def x7_notify(devno, devtype="f02a"):
        message = bytearray(28)
        message[:10] = X7Parser.UDP_START.encode('utf-8')
        cmd = 0x10
        dev_type = 0x38
        port = 54336
        ip = get_ip().split(".")
        
        message[10:12] = cmd.to_bytes(2, 'little')
        dev_id = int(devno, 16)
        message[12:20] = dev_id.to_bytes(8, 'little')
        # message[12:14] = bytes.fromhex(devtype)
        # #d57ee4dc99ce0940        
        # message[14:22] = bytes.fromhex(devno)
        message[22] = (int)(ip[0])
        message[23] = (int)(ip[1])
        message[24] = (int)(ip[2])
        message[25] = (int)(ip[3])
        message[26:28] = port.to_bytes(2, 'little')
        checksum = crc16(message)

        return message + checksum.to_bytes(2, 'little')


def check_crc(data):
    return int.from_bytes(data[-2:], 'little')  == crc16(data[:-2])

def get_data(cmd, packet):
    if cmd == 0x10:
        return packet[12:27]

    return packet[12:] 


def parse_net_param(data):
    dev = DeviceInfo()
    dev.unique_id = data[:10].hex()
    dev.dev_type = data[:2].hex()
    dev.dev_id = data[2:10].hex()
    dev.ip = f"{data[10]}.{data[11]}.{data[12]}.{data[13]}"
    dev.port = int.from_bytes(data[-2:], 'little')

    return dev


import json
class DeviceInfo():
    def __init__(self):
        self.unique_id = None
        self.dev_type = None
        self.dev_id = None
        self.ip = None
        self.port = None

    def __iter__(self):
        yield from {
            "unique_id": self.unique_id,
            "dev_type": self.dev_type,
            "dev_id": self.dev_id,
            "ip": self.ip,
            "port": self.port
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()