from struct import pack
class XDROpaqueSerializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDROpaqueSerializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def serialize(self, value, destination):
        destination.write(struct.pack('>l', len(value)))
        destination.write(value)
        toPad = len(encoded) % 4
        if toPad != 0:
            toPad = 4 - toPad
            destination.write(bytes(toPad))
