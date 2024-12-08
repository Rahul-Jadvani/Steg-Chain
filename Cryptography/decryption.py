from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os

class Decrypter:
    def __init__(self, key):
        """
        Initializes the Decrypter with a key of valid length (16, 24, or 32 bytes).
        """
        # Ensure the key is in bytes
        if isinstance(key, str):
            key = key.encode("utf-8")  # Convert to bytes if it's a string

        # Adjust the key length to 32 bytes (valid for AES)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes long.")
        
        self.key = key

    def decrypt(self, ciphertext):
        """
        Decrypts a ciphertext using AES in CBC mode with PKCS7 padding.
        """
        try:
            iv = ciphertext[:16]  # Extract the first 16 bytes as the IV
            actual_ciphertext = ciphertext[16:]  # The remaining part is the ciphertext
            
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

            # Remove PKCS7 padding
            unpadder = PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            return plaintext
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def decrypt_file(self, file_name):
        """
        Decrypts an encrypted file and writes the decrypted content back to the original file name.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file {file_name} does not exist.")

        try:
            with open(file_name, 'rb') as fo:
                ciphertext = fo.read()  # Read the encrypted file in binary mode

            # Decrypt the file contents
            decrypted_data = self.decrypt(ciphertext)

            original_file_name = file_name[:-4]  # Remove '.enc' extension from file name
            with open(original_file_name, 'wb') as fo:
                fo.write(decrypted_data)

            # Remove the encrypted file
            os.remove(file_name)
            print(f"File decrypted successfully: {original_file_name}")

        except Exception as e:
            raise ValueError(f"Error during file decryption: {str(e)}")
