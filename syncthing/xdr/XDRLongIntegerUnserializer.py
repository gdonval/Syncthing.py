class XDRLongIntegerUnserializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRLongIntegerUnserializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def continueUnserialization(self, data):
        if len(data) < 8:
            return None
        result = int(data[0] << 56 | data[1] << 48 | data[2] << 40 | data[3] << 32 | data[4] << 24 | data[5] << 16 | data[6] << 8 | data[7])
        del(data[0:8])
        return result
