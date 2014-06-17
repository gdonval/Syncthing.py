from syncthing.bep.connection import BEPConnection
import asyncio

class BEPClient(BEPConnection):
    def __init__(self, app, loop):
        super(BEPClient, self).__init__(app, loop)

    @asyncio.coroutine
    def connect(self, destination):
        self.remote_endpoint = destination
        (transport, protocol) = yield from self.loop.create_connection(self.protocol_factory, host=destination[0], port=destination[1], ssl=self.ssl_context)
        try:
            yield from self.app.on_outbound_connect(self)
        except AttributeError:
            # I really do not like this approach. The exception is silenced because 
            # the app method is not mandatory and its non-existence should not crash
            # the application. However, should a real AttributeError -- with another
            # cause land us here, this error silencing will be painful
            #
            # TODO Find a pythonic way to achieve the optional call without this secondary effect
            pass
