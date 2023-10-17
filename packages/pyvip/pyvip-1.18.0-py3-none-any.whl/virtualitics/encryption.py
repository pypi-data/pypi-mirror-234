from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from virtualitics import exceptions
from virtualitics import pkcs7


class VIPCipher:

    def __init__(self, key):
        """
        User-provided key and fixed salt are used to derive key and iv bytes to initialize an
        AES cypher used for encrypting and decrypting.
        :param key: User-provided key string
        """
        self.key = key
        self.salt = '4976616e204d65647665646576'
        self.derived_key = PBKDF2(key, bytes.fromhex(self.salt), 32)
        # IV is split to compensate for .NET's implementation of Rfc2898 GetBytes.
        self.iv = PBKDF2(key, bytes.fromhex(self.salt), 32 + 16)[32:]
        self.encoder = pkcs7.PKCS7Encoder()

    def encrypt(self, raw):
        """
        Raw bytes are encoded using PKCS7 standard padding, and encrypted using the aes cypher.
        :param raw: raw byte array that is to be encrypted
        :returns encrypted: encrypted bytearray
        """
        try:
            raw = self.encoder.encode(raw)
            aes = AES.new(self.derived_key, AES.MODE_CBC, self.iv)
            return aes.encrypt(raw)
        except Exception:
            raise (exceptions.EncryptionException("An error occurred while trying to encrypt your data. See "
                                                  "documentation or consider contacting support@virtualitics.com"))

    def decrypt(self, enc):

        """
        Encrypted bytes are decrypted using the AES cipher and finally decoded (unpadded) using the PKCS7 standard.
        :param enc: encrypted raw data
        :returns decrypted_bytes: unencrypted byte array
        """
        try:
            aes = AES.new(self.derived_key, AES.MODE_CBC, self.iv)
            enc = aes.decrypt(enc)
            return self.encoder.decode(enc)
        except Exception:
            raise (
                exceptions.EncryptionException("An error occurred while trying to decrypt your data. See documentation "
                                               "or consider contacting support@virtualitics.com"))

