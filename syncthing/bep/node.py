from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRIntegerUnserializer import XDRIntegerUnserializer

class BEPNode(BEPSerializable):
    def __init__(self):
        super(BEPNode, self).__init__()
        self.id = None
        self.flags = None

    def nextUnserializer(self):
        if self.id is None:
            return (XDRStringUnserializer(), 'id')
        if self.flags is None:
            return (XDRIntegerUnserializer(), 'flags')
        return None
