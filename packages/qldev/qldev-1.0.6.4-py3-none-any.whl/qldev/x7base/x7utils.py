from qldev.utils import crc16

class CommandEnum():
    GET_DEVICE_INFO = 0x10
    SIGNALS = 0x455
    TRIGGER = 0x501
    WAV_UPDATE_READY = 0x502
    WAV_UPDATE = 0x503
    WAV_UPDATE_STOP = 0x504
    WAV_TRIGGER = 0x505

    
class CommandHeader():
    start = 0xa55a
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get(packet_type=2, dev_type=0, dev_id = 0):
        header = bytearray(12)
        header[:2] = CommandHeader.start.to_bytes(2, 'little')
        header[2] = packet_type
        header[3] = 42
        header[4:8] = dev_id.to_bytes(4, 'little')
        len = 16
        header[8:12] = len.to_bytes(4, 'little')
        # message[12:14] = CommandEnum.GET_DEVICE_INFO.to_bytes(2, 'little')
    

        return  header
    
class DeviceCommand(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_device_info():
        return DeviceCommand.wrap(CommandEnum.GET_DEVICE_INFO)

    @staticmethod
    def header():
        return b'0x5aa5'

    @staticmethod
    def wrap(cmd, data=None):
        header = CommandHeader.get()
        if data:
            dlen = len(data) + 16
            header[8:12] = dlen.to_bytes(4, 'little')
            message = header + cmd.to_bytes(2, 'little') + data 
        else: 
            message = header + cmd.to_bytes(2, 'little')
        
        checksum = crc16(message)
        return message + checksum.to_bytes(2, 'little')

def to_bytes(value, len=4, byteorder = 'little'):
    re = bytearray(len)
    for i in range(len):
        if byteorder == 'little':
            re[i] = (value >> (8 * i)) & 0xFF
        else:
            idx = len - i - 1
            re[idx] = (value >> (8 * i)) & 0xFF
    return re

class X7Command(DeviceCommand):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def trigger(type = 0):
        data = type.to_bytes(4, 'little')
        return DeviceCommand.wrap(CommandEnum.TRIGGER, data)

    @staticmethod
    def wav_update_ready(id, len):
        data = bytearray(8)
        data[:4] = id.to_bytes(4, 'little')
        data[4:] = len.to_bytes(4, 'little')
        return DeviceCommand.wrap(CommandEnum.WAV_UPDATE_READY, data)

    @staticmethod
    def wav_update(id, offset, len, content):
        data = bytearray(len + 12)
        data[:4] = id.to_bytes(4, 'little')
        data[4:8] = offset.to_bytes(4, 'little')
        data[8:12] = len.to_bytes(4, 'little')
        data[12:] = content
        return DeviceCommand.wrap(CommandEnum.WAV_UPDATE, data)

    @staticmethod
    def wav_update_stop(id, md5sum):
        data = id.to_bytes(4, 'little')
        data += md5sum.encode("utf-8") + b'0x0' # 结尾符号解析
        return DeviceCommand.wrap(CommandEnum.WAV_UPDATE_STOP, data)

    @staticmethod
    def wav_trigger(id = 0, volumn = 2):
        data = bytearray(8)
        data[:4] = id.to_bytes(4, 'little')
        data[4:] = volumn.to_bytes(4, 'little')
        return DeviceCommand.wrap(CommandEnum.WAV_TRIGGER, data)