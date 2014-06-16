from syncthing.app.Config import Config
from syncthing.bep.client import BEPClient
from asyncio import Task
class Service(object):
    """A syncthing.app.service is the background service that actually offers 
    the Block Exchange Protocol over the network. It is controllable via 
    RPC mechanisms that have not been defined (or implemented) yet."""


    def __init__(self):
        pass
    
    def getCertificateFiles(self):
        return (Config().get('cert.file'), Config().get('cert.keyfile'))
    
    def start(self, loop):
        """Start the application, using the asyncio event loop passed as parameter.
        This means connecting to known peers, and then starting a server"""
        Task(BEPClient(self, loop).connect(("127.0.0.1", 22000)))

    def on_outbound_connect(self, destination, client_reader, client_writer):
        return []

    def on_outbound_close(self, destination, client_reader, client_writer):
        return []

