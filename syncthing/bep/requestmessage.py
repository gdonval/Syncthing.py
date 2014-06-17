from syncthing.bep.message import BEPMessage
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRIntegerUnserializer import XDRIntegerUnserializer
from syncthing.xdr.XDRLongIntegerUnserializer import XDRLongIntegerUnserializer
from syncthing.xdr.XDRStringSerializer import XDRStringSerializer
from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer
from syncthing.xdr.XDRLongIntegerSerializer import XDRLongIntegerSerializer

class BEPRequestMessage(BEPMessage):
    BEP_TYPE=2
    def __init__(self, messageVersion, messageId):
        super(BEPRequestMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
        self.repository = None
        self.name = None
        self.offset = None
        self.size = None
   
    def nextUnserializer(self):
        if self.repository is None:
            return (XDRStringUnserializer(), 'repository')
        if self.name is None:
            return (XDRStringUnserializer(), 'name')
        if self.offset is None:
            return (XDRLongIntegerUnserializer(), 'offset')
        if self.size is None:
            return (XDRIntegerUnserializer(), 'size')
        return None
    
    def serialize(self, destination):
        super(BEPRequestMessage, self).serialize(destination)
        XDRStringSerializer().serialize(self.repository, destination)
        XDRStringSerializer().serialize(self.name, destination)
        XDRLongIntegerSerializer().serialize(self.offset, destination)
        XDRIntegerSerializer().serialize(self.size, destination)
