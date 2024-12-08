import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from Cryptography import Encrypter  # Assuming `Encrypter` is available in Cryptography module


class KeyGeneration:
    @staticmethod
    def adjust_key_length(key):
        """
        Adjusts the key length to ensure it is 16, 24, or 32 bytes.
        """
        if len(key) not in [16, 24, 32]:
            print(f"Adjusting key length from {len(key)} bytes to 32 bytes.")
            key = key.ljust(32, b'\0')  # Pad with zeroes
        return key

    @staticmethod
    def createkeyfile(keyfile, keyvalue):
        """
        Creates a key file and encrypts it using a randomly generated key.
        """
        directory = os.path.dirname(keyfile)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(keyfile + ".txt", "w+") as f:
            f.write(keyvalue)

        # Generate a 32-byte key for AES-256
        key = os.urandom(32)
        print(f"Generated key (32 bytes): {key.hex()}")

        # Encrypt the file
        Encrypter(key).encrypt_file(keyfile + ".txt")
        return True

    @staticmethod
    def createplaintextfile(plaintextfilename, plaintext):
        """
        Creates a plaintext file and encrypts it using a randomly generated key.
        """
        directory = os.path.dirname(plaintextfilename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(plaintextfilename + ".txt", "w+") as f:
            f.write(plaintext)

        # Generate a 32-byte key for AES-256
        key = os.urandom(32)
        print(f"Generated key (32 bytes): {key.hex()}")

        # Encrypt the file
        Encrypter(key).encrypt_file(plaintextfilename + ".txt")
        return "PlainText File Generated."

    @staticmethod
    def checkforfileexist(filename):
        """
        Checks if an encrypted version of the file exists.
        """
        return os.path.exists(filename + ".txt.enc")
