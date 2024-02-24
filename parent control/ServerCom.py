import queue
import socket
import threading
import select
from queue import Queue
import AES_encrypt


# Import the Key class to handle key exchange using Diffie-Hellman protocol
from Key import *


class ServerComm:

    def __init__(self, port: int, msg_q: Queue):
        # Initialize instance variables
        self.socket = None
        self.port = port
        self.q = msg_q
        self.open_clients = {}  # {socket]: [ip, key, kind]
        self.cp = AES_encrypt.Encrypt(None)
        self.lock = threading.Semaphore()  # create the semaphore lock

        # Start a new thread to run the main loop
        threading.Thread(target=self._main_loop, daemon=True).start()

    def _main_loop(self):
        """
        Connect to clients and handle incoming messages.
        """
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(10)

        while True:
            # Use select to check which sockets are ready to be read from or written to
            rlist, wlist, xlist = select.select([self.socket] + list(self.open_clients.keys()),
                                                list(self.open_clients.keys()), [], 0.01)

            for current_socket in rlist:
                # If the current socket is the server socket, a new client is trying to connect
                if current_socket is self.socket:
                    client, addr = self.socket.accept()
                    ip = addr[0]
                    print(f'{ip} - connected')

                    # Exchange keys with the client using the Diffie-Hellman protocol
                    threading.Thread(target=self._exchange_keys, args=(client, ip), daemon=True).start()

                # If the current socket is a client socket, receive and handle the message
                else:
                    try:
                        # Receive the length of the message and decode it
                        length = int(current_socket.recv(3).decode())
                        # Receive the message and decode it
                        data = current_socket.recv(length).decode()
                        # Decrypt the receive data:
                        self.cp.set_key(self.open_clients[current_socket][1])
                        decrypted_data = self.cp.decrypt(data)
                    except Exception as e:
                        # If an exception occurs, disconnect the client
                        print("ServerComm - _main_loop", str(e))
                        self._disconnect_client(current_socket)
                    else:
                        if data == '':
                            # If the message is empty, disconnect the client
                            self._disconnect_client(current_socket)
                        else:
                            # Put the received message in the message queue along with the client's IP
                            ip = self.open_clients[current_socket][0]
                            self.q.put((decrypted_data, ip))

    def _exchange_keys(self, client_socket, ip):
        """
        Exchange keys with the client using the Diffie-Hellman protocol.
        :param client_socket: the socket object of the client
        :param ip: the ip address of the client
        :return: Noe
        """
        key = Key()  # Create a Key object to handle key exchange
        print("\n-------------key exchange--------------")
        server_public_key = str(key.get_Alice_public_key())  # get the server's public key (A) to send to the client
        print("server_public_key " + server_public_key)
        # send the secret key to the client
        length = str(len(str(server_public_key))).zfill(3)
        print("length - " + length)
        client_socket.send(str(length).encode())
        client_socket.send(server_public_key.encode())

        # Receive the client's public key and compute the secret shared key (B)
        length = int(client_socket.recv(3).decode())  # receive the length
        client_public_key = int(client_socket.recv(length).decode())  # receive the client's public key (B)
        print("client public key: ", client_public_key)
        secret_key = key.compute_key(client_public_key)

        length = int(client_socket.recv(3).decode())  # receive the length
        kind = client_socket.recv(length).decode()

        with self.lock:
            self.open_clients[client_socket] = [ip, secret_key, kind]  # add a new client to the open clients dict
        print(self.open_clients.values())
        print("added a new client to open_clients\nthe key is: ", secret_key)
        print("\n\n")

    def _disconnect_client(self, client_socket):
        """
        disconnect a client by a socket
        :param client_socket: the client' socket
        :return: None
        """
        # use lock
        with self.lock:
            # if  the user exist disconnect him
            if client_socket in self.open_clients.keys():
                print(f'{self.open_clients[client_socket]} - disconnected')
                # if the user is a kid, stop the timer thread
                if self.open_clients[client_socket][2] == 'k':
                    ip = self.find_ip_by_socket(client_socket)
                    self.q.put(("close timer", ip))
                del self.open_clients[client_socket]  # delete the kid from open clients list
                client_socket.close()  # close the socket

    def send(self, data, ip: str):
        """
        send a message
        :param data: the data to send
        :param ip: the ip address to send to
        :return: None
        """
        print("message to send - " + data)

        # check the client to send to the message by the ip from the open clients dict (find the socket by the ip)
        self.lock.acquire()
        for soc in self.open_clients.keys():
            if self.open_clients[soc][0] == ip:
                # send the message
                key = self.open_clients[soc][1]
                encrypted_msg = self.cp.encrypt(data, key)  # encrypt the message to send
                try:
                    soc.send((str(len(encrypted_msg)).zfill(3).encode()))
                    soc.send(encrypted_msg.encode())
                except Exception as e:
                    print("ServerComm - send_specific_client", str(e))
                    self._disconnect_client(soc)
                else:
                    print(f"server sent the message {data}")
        self.lock.release()

    def disconnect_client_by_ip(self, ip):
        """
        disconnect a client by his ip address (from the LOGIC)
        :param ip: the ip address of the client
        :return: None
        """
        soc = self.find_socket_by_ip(ip)
        self._disconnect_client(soc)

    def find_ip_by_socket(self, client_socket):
        """
        finding the ip address of a client by his socket
        :param client_socket: the socket of the client
        :return: the ip address of the client
        """
        ip = None
        # run over all the sockets
        for soc in self.open_clients.keys():
            if soc is client_socket:
                ip = self.open_clients[soc][0]
        return ip

    def find_socket_by_ip(self, client_ip):
        """
        find the socket of a client by his ip address
        :param client_ip: the ip address of the client
        :return: the socket of the client
        """
        client_socket = None
        # run over all the sockets
        for soc in self.open_clients:
            ip = self.open_clients[soc][0]
            if ip is client_ip:
                client_socket = soc
        return client_socket

    def find_kind_by_ip(self, client_ip):
        """
        find the kind of the user by his ip address
        :param client_ip: the ip address of the client
        :return: the kind of the client (p - parent, k-kid)
        """
        kind = None
        # run over all the sockets
        for soc in self.open_clients:
            ip = self.open_clients[soc][0]
            if ip is client_ip:
                kind = self.open_clients[soc][2]
        return kind


if __name__ == '__main__':
    recv_q = queue.Queue()
    comm = ServerComm(1500, recv_q)
    while True:
        data, ip = recv_q.get()
        print(f"data from, {ip}, {data}")
        comm.send(data, ip)