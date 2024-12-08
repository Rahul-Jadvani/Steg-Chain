from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os


class Encrypter:
    def __init__(self, key):
        """
        Initializes the Encrypter with a key of valid length.
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes long.")
        self.key = key

    def encrypt(self, message):
        """
        Encrypts a message using AES in CBC mode with PKCS7 padding.
        """
        iv = os.urandom(16)
        padder = PKCS7(128).padder()
        padded_message = padder.update(message) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        return iv + ciphertext

    def encrypt_file(self, file_name):
        """
        Encrypts a file and appends '.enc' to the encrypted file's name.
        """
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()

        encrypted_data = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(encrypted_data)

        os.remove(file_name)  # Remove the original file
