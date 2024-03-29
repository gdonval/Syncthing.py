from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRIntegerUnserializer import XDRIntegerUnserializer
from syncthing.xdr.XDRStringSerializer import XDRStringSerializer
from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer

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
    
    def serialize(self, destination):
        XDRStringSerializer().serialize(self.id, destination)
        XDRIntegerSerializer().serialize(self.flags, destination)
