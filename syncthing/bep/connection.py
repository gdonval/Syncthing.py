from asyncio import Protocol

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

    def handle_connection(self, endpoint, reader, writer):
        try:
            while True:
                data = yield from reader.readline()
                print(data)
        finally:
            pass
    
    def protocol_factory(self):
        return self

    def connection_made(self, transport):
        self.transport = transport
        try:
            self.app.on_connect(self)
        except AttributeError:
            pass

    def data_received(self, data):
        print(data)
        pass

    def connection_lost(self, exc):
        self.transport = transport
        try:
            self.app.on_disconnect(self, exc)
        except AttributeError:
            pass
        pass
