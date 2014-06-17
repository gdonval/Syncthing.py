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

    def on_outbound_connect(self, connection):
        return []

    def on_outbound_disconnect(self, connection, reason=None):
        return []

    def on_inbound_connect(self, connection):
        return []

    def on_inbound_disconnect(self, connection, reason=None):
        return []

    def on_connect(self, connection):
        return []

    def on_disconnect(self, connection, reason=None):
        return []

    def handle_cluster_config_message(self, connection, msg):
        return []

    def handle_index_message(self, connection, msg):
        return []

    def handle_request_message(self, connection, msg):
        return []

    def handle_response_message(self, connection, msg):
        return []

    def handle_ping_message(self, connection, msg):
        return []

    def handle_pong_message(self, connection, msg):
        return []

