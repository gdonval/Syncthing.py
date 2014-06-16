from syncthing.bep.connection import BEPConnection
import asyncio

class BEPClient(BEPConnection):
    def __init__(self, app, loop):
        super(BEPClient, self).__init__(app, loop)

    @asyncio.coroutine
    def connect(self, destination):
        (transport, protocol) = yield from self.loop.create_connection(self.protocol_factory, host=destination[0], port=destination[1], ssl=self.ssl_context)
