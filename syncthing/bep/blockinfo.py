from syncthing.bep.serializable import BEPSerializable
from syncthing.xdr.XDROpaqueUnserializer import XDROpaqueUnserializer

class BEPBlockInfo(BEPSerializable):
    def __init__(self):
        super(BEPBlockInfo, self).__init__()
        self.hash = None

    def nextUnserializer(self):
        if self.hash is None:
            return (XDROpaqueUnserializer(), 'hash')
        return None
