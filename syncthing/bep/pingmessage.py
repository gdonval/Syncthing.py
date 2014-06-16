from syncthing.bep.message import BEPMessage

class BEPPingMessage(BEPMessage):
    BEP_TYPE=4
    def __init__(self, messageVersion, messageId):
        super(BEPPingMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
   
    def nextUnserializer(self):
        return None
