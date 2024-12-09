from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os

class Decrypter:
    def __init__(self, key):
        # Convert hex string to bytes if the key is a hex string
        if isinstance(key, str):
            self.key = bytes.fromhex(key)
        else:
            self.key = key

        print(f"[DEBUG] Provided key length: {len(self.key)} bytes key value: {self.key}")

        # Ensure the key length is one of the valid AES key sizes (16, 24, 32 bytes)
        if len(self.key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes long.")

    def decrypt(self, ciphertext):
        try:
            # Extract the IV from the first 16 bytes
            iv = ciphertext[:16]
            actual_ciphertext = ciphertext[16:]
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

            # Remove padding
            unpadder = PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return plaintext
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def decrypt_file(self, file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file {file_name} does not exist.")

        try:
            with open(file_name, 'rb') as fo:
                ciphertext = fo.read()
                print(f"[DEBUG] Encrypted key file content (raw bytes): {ciphertext[:32]}")  # Print first 32 bytes for inspection

            decrypted_data = self.decrypt(ciphertext)
            return decrypted_data
        except Exception as e:
            raise ValueError(f"Error during file decryption: {str(e)}")
