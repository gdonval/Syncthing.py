from syncthing.bep.message import BEPMessage
from syncthing.xdr.XDROpaqueUnserializer import XDROpaqueUnserializer

class BEPResponseMessage(BEPMessage):
    BEP_TYPE=3
    def __init__(self, messageVersion, messageId):
        super(BEPResponseMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
        self.data = None
   
    def nextUnserializer(self):
        if self.data is None:
            return (XDROpaqueUnserializer(), 'data')
        return None
