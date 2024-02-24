import random


class Key:
    def __init__(self):
        self.p = 5195977  # choose a large prime number
        self.g = 45345  # choose a primitive root of p
        self.a = random.randint(1, 9999)  # Generate Alice's private key

    def get_Alice_public_key(self):
        """
        get Alice's private key
        :return: the private key
        """
        return (self.g**self.a) % self.p

    def compute_key(self, B):
        """
        compute Alice public key
        :return: the secret shared key between Alice and Bob (server and client)
        """
        return (B**self.a) % self.p