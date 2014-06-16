class XDROpaqueSerializer(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(XDROpaqueSerializer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def serialize(self, value, destination):
        pass
