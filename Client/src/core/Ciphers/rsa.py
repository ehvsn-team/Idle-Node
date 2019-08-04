import os
import sys
import traceback
# Import directives here

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

class Main(object):

    def __init__(self):
        pass

    def generate_key(self, keyfile):
        key = RSA.generate(2048)
        with open(keyfile, 'w') as f:
            f.write(key.exportKey('PEM').decode())

    def encrypt(self, keyfile, data):
        h = SHA.new(data)
        key = RSA.importKey(open(keyfile).read())
        cipher = PKCS1_v1_5.new(key)
        result = cipher.encrypt(message + h.digest())

    def decrypt(self, keyfile, data):
        key = RSA.importKey(open(keyfile).read())
        dsize = SHA.digest_size
        sentinel = Random.new().read(15 + dsize)
        cipher = PKCS1_v1_5.new(key)
        result = cipher.decrypt(data, sentinel)
        digest = SHA.new(result[:-dsize]).digest()
        if digest==result[-dsize:]:
            return [result, True]

        else:
            return [result, False]


class IdleCipher(object):

    def __init__(self):
        pass

    def get_info(self):
        information = {
        "name": "Cipher Name",
        "type": "encryption,signature",
        "description": "Cipher description",
        "encryption_values": {"key": "str", "plaintext": "str"},
        "decryption_values": {"key": "str", "ciphertext": "str:bytes"}
        }

        return information

    def encrypt(self, key, plaintext):
    	return Main().encrypt(key, plaintext)

    def decrypt(self, key, ciphertext):
        return Main().decrypt(key, ciphertext)

    def sign(self, key, data):
        # For signature cipher algorithms only
        return Main().encrypt(key, plaintext)

    def verify(self, key, data):
        # For signature cipher algorithms only
        if Main().decrypt(key, ciphertext)[1] == True:
            return True

        else:
            return False
