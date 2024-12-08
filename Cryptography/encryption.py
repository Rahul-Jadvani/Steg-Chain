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
        # Ensure the message is in bytes
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Generate a random 16-byte IV
        iv = os.urandom(16)

        # Apply PKCS7 padding to the message
        padder = PKCS7(128).padder()
        padded_message = padder.update(message) + padder.finalize()

        # Create the AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt the padded message
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        # Return IV + ciphertext
        return iv + ciphertext

    def encrypt_file(self, file_name):
        """
        Encrypts a file and appends '.enc' to the encrypted file's name.
        """
        # Check if the file exists
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file {file_name} does not exist.")

        try:
            with open(file_name, 'rb') as fo:
                plaintext = fo.read()  # Read the file in binary mode

            encrypted_data = self.encrypt(plaintext)

            # Create the encrypted file with '.enc' extension
            encrypted_file_name = file_name + ".enc"
            with open(encrypted_file_name, 'wb') as fo:
                fo.write(encrypted_data)

            # Remove the original file after encryption
            os.remove(file_name)
            print(f"File encrypted successfully: {encrypted_file_name}")

        except Exception as e:
            raise ValueError(f"Error during file encryption: {str(e)}")

