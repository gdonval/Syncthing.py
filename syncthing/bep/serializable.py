class BEPSerializable(object):
    def __init__(self):
        self.unserializer = None

    def continueUnserialization(self, data):
        if self.unserializer is None:
            self.unserializer = self.nextUnserializer()
        if self.unserializer is None: # None result signals unserialization complete
            return self
        setattr(self, self.unserializer[1], self.unserializer[0].continueUnserialization(data))
        if getattr(self, self.unserializer[1]) is not None: # part serializer returned someting. It is done, unset serializer and continue by recursion
            self.unserializer = None
            return self.continueUnserialization(data)
        return None # part serializer returned None, so it is not finished yet

    def nextUnserializer(self):
        raise Exception('Unimplemented (virtual)')

    def serialize(self, destination):
        raise Exception('Unimplemented (virtual)')
