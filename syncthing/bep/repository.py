from syncthing.bep.serializable import BEPSerializable
from syncthing.bep.node import BEPNode
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRArrayUnserializer import XDRArrayUnserializer
from syncthing.xdr.XDRStringSerializer import XDRStringSerializer
from syncthing.xdr.XDRArraySerializer import XDRArraySerializer

class BEPRepository(BEPSerializable):
    def __init__(self):
        super(BEPRepository, self).__init__()
        self.id = None
        self.nodes = None

    def nextUnserializer(self):
        if self.id is None:
            return (XDRStringUnserializer(), 'id')
        if self.nodes is None:
            return (XDRArrayUnserializer(BEPNode), 'nodes')
        return None
    
    def serialize(self, destination):
        XDRStringSerializer().serialize(self.id, destination)
        XDRArraySerializer().serialize(self.nodes, destination)
