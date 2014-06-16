class XDROpaqueUnserializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDROpaqueUnserializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def continueUnserialization(self, data):
        if len(data) < 4:
            return None
        opaqueLength = int(data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3])
        if opaqueLength % 4 == 0:
            dataLength = opaqueLength
        else:
            dataLength = opaqueLength + 4 - opaqueLength % 4
        if len(data) < dataLength + 4:
            return None
        del(data[0:4])
        result = bytes(data[0:opaqueLength])
        del(data[0:dataLength])
        return result
