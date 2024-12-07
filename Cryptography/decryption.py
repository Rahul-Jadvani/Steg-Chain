from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


class Decrypter:
    def __init__(self, key):
        self.key = key

    def decrypt(self, ciphertext):
        # Ensure the key is 32 bytes (256 bits) for AES-256
        assert len(self.key) == 32, "Key must be 32 bytes long."

        # Extract the IV (first 16 bytes)
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        # Create the cipher
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        # Unpad the plaintext
        unpadder = PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()

        dec = self.decrypt(ciphertext)
        # Uncomment the following lines to write the decrypted content back to a file
        # with open(file_name[:-4], 'wb') as fo:
        #     fo.write(dec)
        # os.remove(file_name)
        return dec
