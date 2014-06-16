class XDRIntegerUnserializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRIntegerUnserializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def continueUnserialization(self, data):
        if len(data) < 4:
            return None
        result = int(data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3])
        del(data[0:4])
        return result
