from syncthing.xdr.XDRIntegerSerializer import XDRIntegerSerializer

class XDRArraySerializer(object):
    def __init__(self, ofclass):
        self.count=XDRIntegerUnserializer()
        self.ofclass = ofclass
        self.result = []
        self.ofunserializer = None

    def continueUnserialization(self, data):
        if isinstance(self.count, XDRIntegerUnserializer):
            candidate = self.count.continueUnserialization(data)
            if candidate is None:
                return None
            self.count = candidate
        if self.count == len(self.result):
            return self.result
        if self.ofunserializer is None:
            self.ofunserializer = self.ofclass()
        candidate = self.ofunserializer.continueUnserialization(data)
        if candidate is None:
            return None
        self.result.append(candidate)
        self.ofunserializer = None
        return self.continueUnserialization(data)
