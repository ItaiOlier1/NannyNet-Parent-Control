from Cryptodome.Cipher import AES
# from crypto.Cipher import AES
from Cryptodome.Hash import SHA256
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Util.Padding import unpad


class Encrypt:
    """
    A class for encrypting and decrypting data using AES CBC mode
    """
    def __init__(self, final_key):
        # initialize with a final key, which can be used for encryption or decryption
        self._global_key = str(final_key)
        self.bs = AES.block_size

    def get_key(self):
        # a getter method for the final key
        return self._global_key

    def set_key(self, new_key):
        self._global_key = str(new_key)

    def encrypt(self, raw, key=None):
        # method to encrypt data
        if key:
            # if a key is passed as a parameter, use it instead of the final key
            key = hashlib.sha256(str(key).encode()).digest()
        else:
            # if no key is provided, use the final key
            key = hashlib.sha256(str(self._global_key).encode()).digest()

        # change the input to bytes if it's a string
        if type(raw) == str:
            raw = raw.encode()

        # pad the data to make it the appropriate length for encryption
        raw = self._pad(raw)

        # generate a random initialization vector (IV) and create a new cipher object
        iv = Random.new().read(self.bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # encrypt the data and combine it with the IV
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc, key=None):
        # method to decrypt data
        if key:
            # if a key is passed as a parameter, use it instead of the final key
            key = hashlib.sha256(key).digest()
        else:
            # if no key is provided, use the final key
            key = hashlib.sha256(self._global_key.encode()).digest()

        # decode the input from base64
        enc = base64.b64decode(enc)

        # separate the IV from the encrypted data
        iv = enc[:self.bs]

        # create a new cipher object and decrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[self.bs:]), self.bs).decode()

    def _pad(self, s):
        """
        Internal method, pads bytes for encryption
        :param s: Bytes to pad
        :return: Padded bytes
        """
        # pad the input with bytes such that its length is a multiple of the block size
        s = (s + (self.bs - len(s) % self.bs) * bytes([self.bs - len(s) % self.bs]))
        return s

    @staticmethod
    def hash(message):
        # static method to compute the SHA-256 hash of a message
        h = SHA256.new()
        h.update(message.encode())
        return h.hexdigest()


if __name__ == '__main__':
    # example usage of the Encrypt class
    key = '2209374'
    cp = Encrypt(key)  # create an instance of the class with the final key
    text = "hello world"
    encrypted = cp.encrypt(text)  # encrypt some data using the final key
    print('encrypt: ', encrypted)
    print('decrypt: ', cp.decrypt(encrypted))  # decrypt the encrypted data using the final key
