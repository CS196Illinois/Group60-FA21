import logging
import pickle

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from Project.global_utils import async_function
from Project.networking.Events.event import Event
from Project.networking.event_handler import EventHandler
from Project.networking.helpers import send_all, recv_all
from Project.networking.twin_client import TwinClient

logger = logging.getLogger(__name__)


class SecureClient(TwinClient):
    def __init__(self, host: str, port: int, session_key: str, event_handler: EventHandler = None):
        super().__init__(host, port, session_key, event_handler)
        self._encryption_cypher = None
        self._decryption_cypher = None

    @property
    def ready(self):
        return super(SecureClient, self).ready and self._encryption_cypher and self._decryption_cypher

    @async_function
    def connect(self):
        """
        Encryption as follows:
        1. Generate public and private RSA keys
        2. Share public RSA key
        3. Await twin public RSA key
        4. Encrypt AES key with twin public key
        5. Share encrypted AES key
        6. Decrypt received AES key with private RSA key

        This allows us to use AES encryption which is significantly faster than RSA, while making sure encryption can't
        be spoofed by third party. Thus we get the asymmetric security with the symmetric speed. Whoa!
        """
        if not super(SecureClient, self).connect.__wrapped__(self):
            return

        # 1. Generate public and private RSA keys
        temp_key = RSA.generate(2048)
        temp_public = temp_key.publickey().export_key()

        # 2. Share public RSA key
        send_all(self._socket, temp_public)

        # 3. Await twin public RSA key
        twin_public = RSA.import_key(recv_all(self._socket))

        # 4. Encrypt AES key with twin public key
        cipher_twin_rsa = PKCS1_OAEP.new(twin_public)
        aes_key = get_random_bytes(16)  # AES key for decryption
        enc_aes_key = cipher_twin_rsa.encrypt(aes_key)

        # 5. Share encrypted AES key
        send_all(self._socket, enc_aes_key)

        # 6. Decrypt received AES key with private RSA key
        cyper_private_rsa = PKCS1_OAEP.new(temp_key)
        twin_aes_key = cyper_private_rsa.decrypt(recv_all(self._socket))  # AES key for encryption

        # We use our own key (reversed) as the initiation vector for the encryption cypher.
        self._encryption_cypher = AES.new(twin_aes_key, AES.MODE_CBC, iv=aes_key[::-1])
        self._decryption_cypher = AES.new(aes_key, AES.MODE_CBC, iv=twin_aes_key[::-1])
        print("Connected")

    def send(self, event: Event):
        if not self.ready:
            logger.warning(f"Connection not ready")
            return
        send_all(self._socket, self._encryption_cypher.encrypt(pad(event.pickle(), AES.block_size)))

    def recv(self):
        if not self.ready:
            logger.warning(f"Connection not ready")
            return
        try:
            event = pickle.loads(unpad(self._decryption_cypher.decrypt(recv_all(self._socket)), AES.block_size))
        except pickle.UnpicklingError:
            logger.warning(f"Unable to decryption or deserialize event")
            return
        if isinstance(event, KeyChangeEvent):
            self._on_change_key(event.key, event.iv)
            print(f"Key changed to {event.key}")
            event.dispose()
            return
        return event

    def _on_change_key(self, key: bytes, iv: bytes):
        self._decryption_cypher = AES.new(key, AES.MODE_CBC, iv=iv)

    def change_key(self):
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        self.send(KeyChangeEvent(key, iv))
        self._encryption_cypher = AES.new(key, AES.MODE_CBC, iv=iv)
        print(f"Changing key to {key}")


class KeyChangeEvent(Event):
    def __init__(self, key: bytes, iv: bytes):
        super(KeyChangeEvent, self).__init__()
        self.key = key
        self.iv = iv

