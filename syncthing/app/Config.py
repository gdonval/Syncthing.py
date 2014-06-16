class Config(object):
    _instance = None

    def __new__(cls, *args, **kwargs): # This may be a singleton
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get(self, key):
        if key == "cert.file":
            import os
            import sys
            return sys.path[1] + os.sep + "data" + os.sep + "cert.pem"
        if key == "cert.keyfile":
            import os
            import sys
            return sys.path[1] + os.sep + "data" + os.sep + "key.pem"
        raise Exception("Unknown config key %s" % (key))
