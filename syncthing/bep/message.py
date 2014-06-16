from syncthing.bep.serializable import BEPSerializable

class BEPMessage(BEPSerializable):
    def __init__(self, messageVersion, messageType, messageId):
        super(BEPMessage, self).__init__()
        self.version = messageVersion
        self.type = messageType
        self.id = messageId
