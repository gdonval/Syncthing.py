class XDRStringUnserializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRStringUnserializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def continueUnserialization(self, data):
        if len(data) < 4:
            return None
        stringLength = int(data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3])
        if stringLength % 4 == 0:
            dataLength = stringLength
        else:
            dataLength = stringLength + 4 - stringLength % 4
        if len(data) < dataLength + 4:
            return None
        del(data[0:4])
        result = bytes(data[0:stringLength]).decode('utf-8')
        del(data[0:dataLength])
        return result
