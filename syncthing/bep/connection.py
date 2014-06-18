from asyncio import Protocol,coroutine,Task
from zlib import decompressobj, compressobj, MAX_WBITS, Z_DEFAULT_COMPRESSION, DEFLATED,Z_SYNC_FLUSH
from syncthing.bep.message import BEPMessage
from syncthing.bep.clusterconfigmessage import BEPClusterConfigMessage
from syncthing.bep.indexmessage import BEPIndexMessage
from syncthing.bep.requestmessage import BEPRequestMessage
from syncthing.bep.responsemessage import BEPResponseMessage
from syncthing.bep.pingmessage import BEPPingMessage
from syncthing.bep.pongmessage import BEPPongMessage
from syncthing.bep.indexupdatemessage import BEPIndexUpdateMessage
from syncthing.xdr.XDRIntegerUnserializer import XDRIntegerUnserializer

class BEPConnection(Protocol):
    def __init__(self, app, loop):
        self._ssl_context = None
        self.app = app
        self.loop = loop
    
    def get_ssl_context(self):
        if self._ssl_context is None:
            import ssl
            certFiles = self.app.getCertificateFiles()
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            self._ssl_context.verify_mode = ssl.CERT_NONE
            self._ssl_context.set_ciphers('DHE-RSA-AES256-GCM-SHA384,DHE-RSA-AES256-SHA256,ECDHE-RSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-SHA384,DHE-RSA-AES128-GCM-SHA256,DHE-RSA-AES128-SHA256,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-SHA256')
            self._ssl_context.load_cert_chain(certFiles[0], certFiles[1])
            self._ssl_context.load_verify_locations(certFiles[0])
        return self._ssl_context
    ssl_context = property(get_ssl_context, None, None, None)

    def message_factory(self, messageVersion, messageType, messageId):
        if messageType == BEPClusterConfigMessage.BEP_TYPE:
            return BEPClusterConfigMessage(messageVersion, messageId)
        if messageType == BEPIndexMessage.BEP_TYPE:
            return BEPIndexMessage(messageVersion, messageId)
        if messageType == BEPRequestMessage.BEP_TYPE:
            return BEPRequestMessage(messageVersion, messageId)
        if messageType == BEPResponseMessage.BEP_TYPE:
            return BEPResponseMessage(messageVersion, messageId)
        if messageType == BEPPingMessage.BEP_TYPE:
            return BEPPingMessage(messageVersion, messageId)
        if messageType == BEPPongMessage.BEP_TYPE:
            return BEPPongMessage(messageVersion, messageId)
        if messageType == BEPIndexUpdateMessage.BEP_TYPE:
            return BEPIndexUpdateMessage(messageVersion, messageId)
        raise Exception("Unknown message type received: " + str(messageType))

    
    def protocol_factory(self):
        return self

    def connection_made(self, transport):
        self.transport = transport
        self.decompressor = decompressobj(-MAX_WBITS)
        self.compressor = compressobj(level=Z_DEFAULT_COMPRESSION, method=DEFLATED, wbits=-MAX_WBITS)
        self.unused_data = bytearray()
        self.incoming_message = None

        try:
            self.app.on_connect(connection=self)
        except AttributeError:
            # I really do not like this approach. The exception is silenced because 
            # the app method is not mandatory and its non-existence should not crash
            # the application. However, should a real AttributeError -- with another
            # cause land us here, this error silencing will be painful
            #
            # TODO Find a pythonic way to achieve the optional call without this secondary effect
            pass

    def data_received(self, data):
        self.unused_data += self.decompressor.decompress(data)
        self.consume_unused_data()

    def consume_unused_data(self):
        if self.incoming_message is None and len(self.unused_data) >= 4:
            toUnpack = XDRIntegerUnserializer().continueUnserialization(self.unused_data)
            messageVersion = (toUnpack>>28) & 0xf
            messageId = (toUnpack>>16) & 0xfff
            messageType = (toUnpack>>8) & 0xff
            self.incoming_message = self.message_factory(messageVersion, messageType, messageId)

        if self.incoming_message is not None:
            candidate = self.incoming_message.continueUnserialization(self.unused_data)
            if candidate is not None: # Unserialization is complete
                self.incoming_message = None
                result = []
                result.append(candidate)
                candidate = self.consume_unused_data()
                if candidate is not None:
                    result.append(candidate)
                tasks = [Task(self.message_received(msg), loop=self.loop) for msg in result]

    def connection_lost(self, exc):
        try:
            self.app.on_disconnect(connection=self, reason=exc)
        except AttributeError:
            # I really do not like this approach. The exception is silenced because 
            # the app method is not mandatory and its non-existence should not crash
            # the application. However, should a real AttributeError -- with another
            # cause land us here, this error silencing will be painful
            #
            # TODO Find a pythonic way to achieve the optional call without this secondary effect
            pass
        pass

    @coroutine
    def message_received(self, msg):
        if type(msg) is BEPClusterConfigMessage:
            yield from self.app.handle_cluster_config_message(self, msg)
        if type(msg) is BEPIndexMessage:
            yield from self.app.handle_index_message(self, msg)
        if type(msg) is BEPRequestMessage:
            yield from self.app.handle_request_message(self, msg)
        if type(msg) is BEPResponseMessage:
            yield from self.app.handle_response_message(self, msg)
        if type(msg) is BEPPingMessage:
            yield from self.app.handle_ping_message(self, msg)
        if type(msg) is BEPPongMessage:
            yield from self.app.handle_pong_message(self, msg)
        yield from []

    def write(self, data, flush=True):
        """Send the data through the connection

        This method acts simultaneously like a transport write() and a protocol write(). A
        protocol write() receives a BEPMessage object and sends it. A transport write receives
        a byte-ish argument and sends it. The transport behaviour is alien here, it should be 
        embedded in the asyncio transport. It isn't because those are not easily extensible,
        and BEP requires zlib compression of the SSL transport stream.

        Long story short: expected usage is as a protocol write(). Pass in a BEPMessage and it 
        will be sent to the remote endpoint.

        Arguments:
        data -- An instance of a BEPMessage, to be sent
        """
        if not isinstance(data, (bytes, bytearray, memoryview, BEPMessage)):
            raise TypeError('data argument must be byte-ish or a BEPMessage (%r)', type(data))
        if isinstance(data, BEPMessage):
            return data.serialize(self)
        print("Writing:" + str(data))
        compressed = self.compressor.compress(data)
        if flush:
            compressed += self.compressor.flush(Z_SYNC_FLUSH)
        if len(compressed) > 0:
            print("Writing (compressed):" + str(compressed))
            self.transport.write(compressed)

