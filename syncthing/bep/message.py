from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer

class BEPMessage(BEPSerializable):
    def __init__(self, messageVersion, messageType, messageId):
        super(BEPMessage, self).__init__()
        self.version = messageVersion
        self.type = messageType
        self.id = messageId

    def serialize(self, destination):
        XDRIntegerSerializer().serialize( 
            (self.version & 0xf << 28) |
            (self.id & 0xfff << 16) |
            (self.type & 0xff << 8),
            destination)
