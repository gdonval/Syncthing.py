from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRStringSerializer import XDRStringSerializer

class BEPOption(BEPSerializable):
    def __init__(self):
        super(BEPOption, self).__init__()
        self.key = None
        self.value = None

    def nextUnserializer(self):
        if self.key is None:
            return (XDRStringUnserializer(), 'key')
        if self.valye is None:
            return (XDRStringUnserializer(), 'value')
        return None

    def serialize(self, destination):
        XDRStringSerializer().serialize(self.key, destination)
        XDRStringSerializer().serialize(self.value, destination)
