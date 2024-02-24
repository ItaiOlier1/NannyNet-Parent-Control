import queue
import socket
import threading
from queue import Queue
from Key import Key
import AES_encrypt
import time


class ClientComm:
    """
    class to represent client (communication)
    """

    def __init__(self, server_ip: str, port: int, msg_q: Queue, kind):
        """
        init the object
        :param server_ip: server ip
        :param port: port of communication
        :param msg_q: the messages queue
        """
        self.handle_key = Key()  # an object to switch keys
        self.socket = None  # the socket
        self.server_ip = server_ip  # the ip address of the server
        self.port = port  # the communication port
        self.client_q = msg_q  # the q to communicate with the logic
        self.secret_key = -1  # the encryption key
        self.kind = kind  # the kind of the client (p - parent, k - kid)
        self._connect()  # connect to the server
        self.cp = AES_encrypt.Encrypt(self.secret_key)
        threading.Thread(target=self._main_loop, daemon=True).start()

    def _connect(self):
        self.socket = socket.socket()
        try:
            self.socket.connect((self.server_ip, self.port))
        except Exception as e:
            print("ClientComm - _connect", str(e))
            exit()
        else:
            print("CONNECTED")
            # send the private key to the server to set communication:

            my_public_key = str(self.handle_key.get_Alice_public_key())
            print("public key - " + str(my_public_key))
            length = str(len(str(my_public_key))).zfill(3)
            try:
                self.socket.send(str(length + my_public_key).encode())
                length = int(self.socket.recv(3).decode())
                print("length - ", length)
                data = self.socket.recv(length).decode()
                length = str(len(str(self.kind))).zfill(3)
                self.socket.send((length + self.kind).encode())
            except Exception as e:
                print("ClientComm - _connect", str(e))
                exit()

            else:
                # if the client has no key for communication yet, set the receive data as the key
                if self.secret_key == -1:
                    print("server public key: ", int(data))
                    self.secret_key = self.handle_key.compute_key(int(data))
                    print("the secret key is:", self.secret_key)

    def _main_loop(self):
        """
        get data from server
        :return:
        """
        while True:
            try:
                # Receive the length of the message and decode it
                length = int(self.socket.recv(3).decode())
                # Receive the message and decode it
                data = self.socket.recv(length).decode()
                # Decrypt the receive data:
                decrypted_data = self.cp.decrypt(data)

            except Exception as e:
                print("ClientComm - _main_loop", str(e))
                exit()
            else:
                if data == "":
                    exit()
                self.client_q.put(decrypted_data)

    def send(self, msg):
        """
        send a message to the server
        :param msg: the message to send
        :return: None
        """
        encrypted_msg = self.cp.encrypt(msg)
        try:
            self.socket.send((str(len(encrypted_msg)).zfill(3).encode()))
            self.socket.send(encrypted_msg.encode())
        except Exception as e:
            print("ClientComm - send", str(e))
            exit()


if __name__ == '__main__':

    q = queue.Queue()
    com = ClientComm("192.168.0.117", 1500, q, "p")
    com.send("Hello world")

    while True:
        data = q.get()
        print("data from server: ", data)
