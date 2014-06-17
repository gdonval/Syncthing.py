from struct import pack
from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer

class XDRArraySerializer(object):
    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDRArraySerializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def serialize(self, value, elementClass, destination):
        destination.write(struct.pack('>l', len(value)))
        for elm in value:
            elementClass().serialize(elm, destination)
