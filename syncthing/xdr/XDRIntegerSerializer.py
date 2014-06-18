from struct import pack
class XDRIntegerSerializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRIntegerSerializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def serialize(self, value, destination):
        destination.write(pack('>l', value))
