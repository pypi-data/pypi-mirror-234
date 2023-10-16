import ssl
from grpclib.client import Channel as gRPClibChannel
from tempfile import mkstemp
from .device_ca_cert import ca_cert
from grpclib.events import SendRequest, listen
import inspect
import os


class Channel(gRPClibChannel):
    """
    Channel class is used to securely connect to a Qb2 device.

    The connection is encrypted and authenticated.
    The serial_number can be passed additionally to authenticate a particular device.
    If it is not supplied, the authentication only checks if it is a Blickfeld device.

    ::param fqdn_or_ip: Fully qualified domain name e.g. qb2-xxxxx.blickfeld.com, hostname, or IP address
    :type fqdn_or_ip: str
    param serial_number: Unique serial number assigned to each Qb2 device (corresponding serial number is written on the device label)
    :type serial_number: str
    :param port: Port on which the Qb2 device is reachable (the default is 55551)
    :type port: uint
    :param device_ca_cert: String containing a root certificate for SSL connection
    :type device_ca_cert: str
    :param token: String containing an access token or an awaitable which is called on every method call
    """

    def __init__(
        self, fqdn_or_ip: str, serial_number: str = None, port=55551, device_ca_cert=ca_cert, token=None, metadata=None
    ) -> None:
        # Store all properties to allow clone
        self.fqdn_or_ip = fqdn_or_ip
        self.serial_number = serial_number
        self.port = port
        self.device_ca_cert = device_ca_cert
        self.token = token
        self.metadata = metadata

        # save device ca certificate key to temporal file
        fd, key_and_cert_file = mkstemp()
        with open(fd, "w") as f:
            f.write(device_ca_cert)

        # create SSL context for client
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # client side context
        ctx.verify_mode = ssl.CERT_REQUIRED  # TLS
        ctx.check_hostname = False  # disable hostname check
        ctx.set_alpn_protocols(["h2"])
        try:
            ctx.load_verify_locations(cafile=key_and_cert_file)
        except ssl.SSLError as error:
            raise RuntimeError("Device CA certificate is of incorrect format:" + error.reason)

        # TODO This always uses insecure connections as there is not detection yet
        #      which checks if a secure connection would work.
        if os.getenv("BF_ALLOW_INSECURE_CONNECTIONS") is not None:
            print(f"Using insecure connection to {fqdn_or_ip} as BF_ALLOW_INSECURE_CONNECTIONS is set")
            port = 50051
            ctx = None

        # TODO Check serial number. Authentication of device serial number is not yet implemented.

        # establish gRPC secured channel
        super().__init__(host=fqdn_or_ip, port=port, ssl=ctx)
        # if token is provided -> inject it to every outgoing send request
        if token:
            listen(self, SendRequest, self.__inject_token)

        if metadata:
            listen(self, SendRequest, self.__inject_metadata)

    def clone(self, token=None):
        return Channel(
            fqdn_or_ip=self.fqdn_or_ip,
            serial_number=self.serial_number,
            port=self.port,
            device_ca_cert=self.device_ca_cert,
            token=token if token != self.token else self.token,
            metadata=self.metadata,
        )

    async def __inject_token(self, event: SendRequest):
        # if token is method, call it to get token
        token = self.token
        if callable(token):
            token = token(self)
        if inspect.isawaitable(token):
            token = await token
        event.metadata["token"] = token

    async def __inject_metadata(self, event: SendRequest):
        event.metadata.update(self.metadata)

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        self.close()

    # Allow synchronous usage
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
