import json
import random
import socket
import threading

from pyile_protocol.lib.utils import *
from pyile_protocol.lib.messenger.Messenger import Messenger


def msg_pass(data):
    if data == "":
        return False
    elif data == "\n":
        return False
    elif data == " ":
        return False
    return True


class Peer:
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------

    ENCODE : str
        The encoding used to encode and decode messages
    BUFFER : int
        The buffer size used to send and receive messages
    disconnected : bool
        A boolean to represent if the peer is disconnected
    threads : list
        A list of threads that are running or have run
    address : tuple
        A tuple of the address and port of the peer
    auth_socket : socket
        The socket used to authenticate peers
    peer_address : tuple
        A tuple of the address and port of the communication socket
    peer_socket : socket
        The socket used to communicate with other non-initial peers
    peers : list
        A list of all the peers in the network

    Methods
    -------
    __init__(address)
        Constructor for the Peer class
    __str__()
        Returns a string representation of the peer
    handle_peer(addr)
        Helper function for connect() to handle peer connections
    connect()
        connect() is threaded method that lists for incoming peer connections
        that have already been authenticated
    broadcast(data)
        Broadcasts a message to all peers in the network.
    send(address, data)
        Sends a message to a specific peer
    leave()
        Leaves the network and closes all sockets along with joining all threads.



    """

    def __init__(self, address, messenger, alias):
        if type(self) == Peer:
            raise TypeError("Peer cannot be directly instantiated")

        self.BUFFER = 2048
        self.disconnected = False
        self.threads = []

        self.address = address
        self.auth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.auth_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.auth_socket.settimeout(4)
        self.auth_socket.bind(self.address)

        self.dist_address = (self.address[0], 50000 + random.randint(0, 1000))
        self.dist_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dist_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dist_socket.settimeout(4)
        self.dist_socket.bind(self.dist_address)

        self.peer_address = (self.address[0], 49000 + random.randint(0, 1000))
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.settimeout(4)
        self.peer_socket.bind(self.peer_address)

        self.peers = []
        self.alias = alias
        self.messenger = messenger

    def __str__(self):
        return f"Peer at {self.address}"

    def handle_peer(self, addr):
        """
        Helper function for connect() to handle peer connections

        Parameters
        ----------
        addr

        Returns
        -------

        """
        data = recv_json(addr.recv(self.BUFFER))
        self.messenger.add_message(data)
        addr.send(send_json({
            "data": data,
            "alias": self.alias
        }))

    def connect(self):
        """
        connect() is threaded method that listens for incoming peer connections
        that have already been authenticated

        Returns
        -------

        """
        try:
            self.peer_socket.listen()
        except:
            pass
        while not self.disconnected:
            try:
                addr, acc_connect = self.peer_socket.accept()
                for peer in self.peers:
                    if peer[0] == addr.getpeername()[0]:
                        self.handle_peer(addr)
            except:
                pass

    def broadcast(self, data):
        """
        Broadcasts a message to all peers in the network.

        Parameters
        ----------
        data

        Returns
        -------

        """
        if msg_pass(data):
            json_msg = {}
            for peer in self.peers:
                if peer != self.peer_address:
                    print("broadcast:", peer)
                    json_msg = self.send(peer, data, "Broadcast")

            json_msg["self"] = True
            self.messenger.add_message(json_msg)

    def send(self, address, data, receiver):
        if address == self.peer_address:
            self.messenger.add_warning("Cannot send to self")
            return
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
            send_sock.settimeout(2)
            try:
                send_sock.connect(address)
                json_msg = {
                    "data": data,
                    "alias": self.alias,
                    "to": receiver,
                    "from": self.peer_address
                }
                send_sock.send(send_json(json_msg))
                if receiver != "Broadcast":
                    json_msg["self"] = True
                    self.messenger.add_message(json_msg)
                return json_msg
            except Exception as e:
                send_sock.close()
                self.messenger.add_info("Peer at " + str(address) + " is not responding: " + str(e))

    def leave(self):
        """
        Leaves the network

        Returns
        -------

        """
        if type(self.auth_socket) == socket.socket:
            self.auth_socket.close()
        if type(self.peer_socket) == socket.socket:
            self.peer_socket.close()
        if type(self.dist_socket) == socket.socket:
            self.dist_socket.close()
        join_threads(self.threads)
        self.disconnected = True
