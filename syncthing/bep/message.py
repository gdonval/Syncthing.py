from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer

class BEPMessage(BEPSerializable):
    _next_available_id = 0
    @staticmethod
    def next_available_id():
        return BEPMessage._next_available_id

    def _get_id(self):
        return self._id
    def _set_id(self, value):
        if abs(value - BEPMessage._next_available_id < 2048): # If the message ID has rolled over, do not revert the rollover
            BEPMessage._next_available_id = max(value+1, BEPMessage._next_available_id)
        if BEPMessage._next_available_id > 4096:
            BEPMessage._next_available_id = 0
        self._id = value
    def _del_id(self):
        del self._id
    id = property(_get_id, _set_id, _del_id, None)

    def __init__(self, messageVersion, messageType, messageId=None):
        super(BEPMessage, self).__init__()
        if messageId is None:
            messageId = BEPMessage.next_available_id()
        self.version = messageVersion
        self.type = messageType
        self.id = messageId

    def serialize(self, destination):
        XDRIntegerSerializer().serialize( 
            ((self.version & 0xf) << 28) |
            ((self.id & 0xfff) << 16) |
            ((self.type & 0xff) << 8),
            destination)
