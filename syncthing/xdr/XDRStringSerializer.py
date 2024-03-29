from struct import pack
class XDRStringSerializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRStringSerializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def serialize(self, value, destination):
        encoded = value.encode('utf-8')
        destination.write(pack('>l', len(encoded)))
        destination.write(encoded)
        toPad = len(encoded) % 4
        if toPad != 0:
            toPad = 4 - toPad
            destination.write(bytes(toPad))
