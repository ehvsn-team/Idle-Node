try:
	import os
	import sys

	import traceback

	# Import directives here

except Exception as e:
	return 10, [e, traceback.format_exc()]

class IdleCipher(object):

    def __init__(self):
        pass

    def get_info(self):
        information = {
        "name": "Cipher Name",
        "description": "Cipher description",
        "encryption_values": {"key": "str", "plaintext": "str"},
        "decryption_values": {"key": "str", "ciphertext": "str:bytes"}
        }

        return information

    def encrypt(self, key, plaintext):
    	return key + plaintext[::-1] + key

    def decrypt(self, key, ciphertext):
        return plaintext.replace(key, "")[::1]
