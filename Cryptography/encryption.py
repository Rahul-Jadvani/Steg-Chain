from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os


class Encrypter:
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        # Ensure the key is 32 bytes (256 bits) for AES-256
        assert len(self.key) == 32, "Key must be 32 bytes long."

        # Initialize a random IV
        iv = os.urandom(16)

        # Pad the message to ensure it's a multiple of the block size
        padder = PKCS7(128).padder()
        padded_message = padder.update(message) + padder.finalize()

        # Create the cipher
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        return iv + ciphertext

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()

        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)
