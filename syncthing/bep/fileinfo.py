from syncthing.bep.serializable import BEPSerializable
from syncthing.bep.blockinfo import BEPBlockInfo
from syncthing.xdr.XDRStringUnserializer import XDRStringUnserializer
from syncthing.xdr.XDRIntegerUnserializer import XDRIntegerUnserializer
from syncthing.xdr.XDRLongIntegerUnserializer import XDRLongIntegerUnserializer
from syncthing.xdr.XDRArrayUnserializer import XDRArrayUnserializer

class BEPFileInfo(BEPSerializable):
    def __init__(self):
        super(BEPFileInfo, self).__init__()
        self.name = None
        self.flags = None
        self.modified = None
        self.version = None
        self.blocks = None

    def nextUnserializer(self):
        if self.name is None:
            return (XDRStringUnserializer(), 'name')
        if self.flags is None:
            return (XDRIntegerUnserializer(), 'flags')
        if self.modified is None:
            return (XDRLongIntegerUnserializer(), 'modified')
        if self.version is None:
            return (XDRLongIntegerUnserializer(), 'version')
        if self.blocks is None:
            return (XDRArrayUnserializer(BEPBlockInfo), 'blocks')
        return None
