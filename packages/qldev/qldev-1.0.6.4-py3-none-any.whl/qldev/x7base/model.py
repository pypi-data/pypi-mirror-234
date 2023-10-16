class X7EEG(object):
    def __init__(self, data) :
        self._data = data
        self.info = {}

    def _parse(self, data):        
        self.info["packet_id"] = int.from_bytes(data[:8], 'little')
        self.info["channels"] = data[17:49]
        self.info["origin_rate"] = int.from_bytes(data[49:53], 'little')
        self.info["sample_rate"] = int.from_bytes(data[53:57], 'little')
        self.info["sample_length"] = int.from_bytes(data[57:61], 'little')
        self.info["resolution"] = int.from_bytes(data[61:63], 'little')
        self.info["filter"] = int.from_bytes(data[63], 'little')
        self.info["date_len"] = int.from_bytes(data[64:68], 'little')

class EEGContainer(object):
    def __init__(self) -> None:
        pass

    def append(self, data):
        eeg = X7EEG(data)
        return


