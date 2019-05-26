import os
import sys

import base64
import hashlib
try:
    from Crypto import Random
    from Crypto.Cipher import AES

except ImportError:
    # Prints if error is encountered while importing modules.
    print("Import Error!")
    print()
    print("==================== TRACEBACK ====================")
    traceback.print_exc()
    print("===================================================")
    sys.exit(1)


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class IdleCipher(object):

    def __init__(self):
        pass

    def get_info(self):
        information = {
        "name": "AES",
        "description": "The AES encryption and decryption module.",
        "encryption_values": {"key": "str", "plaintext": "str"},
        "decryption_values": {"key": "str", "ciphertext": "str:bytes"}
        }

        return information

    def encrypt(self, key, plaintext):
        return AESCipher(key).encrypt(plaintext)

    def decrypt(self, key, ciphertext):
        return AESCipher(key).decrypt(ciphertext)
