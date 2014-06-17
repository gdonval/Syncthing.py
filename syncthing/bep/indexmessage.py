from syncthing.bep.message import BEPMessage
from syncthing.bep.fileinfo import BEPFileInfo
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRArrayUnserializer import XDRArrayUnserializer
from syncthing.xdr.XDRStringSerializer import XDRStringSerializer
from syncthing.xdr.XDRArraySerializer import XDRArraySerializer

class BEPIndexMessage(BEPMessage):
    BEP_TYPE=1
    def __init__(self, messageVersion, messageId):
        super(BEPIndexMessage, self).__init__(messageVersion, self.BEP_TYPE, messageId)
        self.repository = None
        self.files = None
   
    def nextUnserializer(self):
        if self.repository is None:
            return (XDRStringUnserializer(), 'repository')
        if self.files is None:
            return (XDRArrayUnserializer(BEPFileInfo), 'files')
    
    def serialize(self, destination):
        super(BEPIndexMessage, self).serialize(destination)
        XDRStringSerializer().serialize(self.repository, destination)
        XDRArraySerializer().serialize(self.files, destination)
