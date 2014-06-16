from syncthing.bep.message import BEPMessage
from syncthing.bep.repository import BEPRepository
from syncthing.bep.option import BEPOption
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRArrayUnserializer import XDRArrayUnserializer

class BEPClusterConfigMessage(BEPMessage):
    BEP_TYPE=0
    def __init__(self, messageVersion, messageId):
        super(BEPClusterConfigMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
        self.clientName = None
        self.clientVersion = None
        self.repositories = None
        self.options = None
   
    def nextUnserializer(self):
        if self.clientName is None:
            return (XDRStringUnserializer(), 'clientName')
        if self.clientVersion is None:
            return (XDRStringUnserializer(), 'clientVersion')
        if self.repositories is None:
            return (XDRArrayUnserializer(BEPRepository), 'repositories')
        if self.options is None:
            return (XDRArrayUnserializer(BEPOption), 'options')
