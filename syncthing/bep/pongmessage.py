from syncthing.bep.message import BEPMessage

class BEPPongMessage(BEPMessage):
    BEP_TYPE=5
    def __init__(self, messageVersion, messageId):
        super(BEPPongMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
   
    def nextUnserializer(self):
        return None
