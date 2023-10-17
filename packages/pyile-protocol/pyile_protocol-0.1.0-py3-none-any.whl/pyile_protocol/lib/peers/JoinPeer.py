import threading
import time

from pyile_protocol.lib.peers.Peer import Peer
from pyile_protocol.lib.utils import *
from pyile_protocol.lib.error import *


class JoinPeer(Peer):
    """
    Child class of Peer Class. Used to join a network and get authentication from an initial peer.
    ...

    Attributes
    ----------

    auth_peer : tuple of (ip, port)

    Methods
    -------
    __init__(address)
        Constructor for JoinPeer class.
    get_authenticated(starting_address, password)
        The first method that should be called when a JoinPeer is created.
    recv_status()
        Establishes and maintains a heart beat from the auth peer.
    """

    def __init__(self, address, messenger, alias):
        Peer.__init__(self, address=address, messenger=messenger, alias=alias)
        self.auth_peer = None

    def _password_check(self, password, starting_address):
        """
        Helper function that checks the password.

        :return: True if authenticated

        """
        try:
            self.auth_socket.send(send_json({"shadow": password}))
            pw_status = recv_json(self.auth_socket.recv(self.BUFFER))
            if pw_status["authenticated"]:
                self.messenger.add_info("Password is correct")
                # adding auth peer
                self.auth_peer = starting_address
                # sends new socket to auth peer
                self.auth_socket.send(send_json({"peer_address": self.peer_address}))
                # receives peers from auth peer
                recv_peers = recv_json(self.auth_socket.recv(self.BUFFER))
                self.peers = to_tuple(recv_peers["distro"])
                return True
            elif not pw_status["authenticated"]:
                raise AuthenticationException("Password is incorrect")
        except AuthenticationException as e:
            self.messenger.add_warning(e)
            self.leave()
            return False

    def get_authenticated(self, starting_address, password):
        """
        The first method that should be called when a peer is created.
        connects to initial peer and authenticates with password.
        :param starting_address: tuple of (ip, port)
        :param password: string
        :return: True if authenticated, False if not
        """

        # Connect to initial peer
        try:
            self.auth_socket.connect(starting_address)
        except ConnectionRefusedError:
            self.auth_socket.close()

        # Receive banned status from initial peer
        try:
            recv_banned = self.auth_socket.recv(self.BUFFER)
            banned = recv_json(recv_banned)
            self.messenger.add_info("Banned Status: " + str(banned["banned"]))
            if banned["banned"]:
                raise AuthenticationException("You are banned from this network")
        except AuthenticationException as e:
            self.messenger.add_error(e)
            self.leave()
            return
        # Performs password check
        authenticated = self._password_check(password, starting_address)
        if authenticated:
            dist_response = recv_json(self.auth_socket.recv(self.BUFFER))
            self.messenger.add_info("auth_dist_addr: " + str(tuple(dist_response["dist_addr"])))
            try:
                self.dist_socket.connect(tuple(dist_response["dist_addr"]))
            except ConnectionException as e:
                self.messenger.error("could not connect to: " + str(tuple(dist_response["dist_addr"])) + ": " + str(e))
                self.dist_socket.close()
            recv_thread = threading.Thread(target=self.recv_status)
            dist_thread = threading.Thread(target=self.recv_dist)
            try:
                dist_thread.start()

            except ThreadException:
                pass
            try:
                recv_thread.start()

            except ThreadException:
                pass

        return authenticated

    def recv_dist(self):
        while not self.disconnected:
            try:
                beat = self.dist_socket.recv(self.BUFFER * 10)
                if beat:
                    json_beat = recv_json(beat)
                    if "distro" in json_beat:
                        self.peers = to_tuple(json_beat["distro"])
                        self.messenger.add_info("Auth peer sent a new set: " + str(self.peers))
            except:
                pass
        self.leave()

    def recv_status(self):
        """
        Establishes and maintains a heart beat from the auth peer.

        :return:

        """
        while not self.disconnected:
            try:
                self.auth_socket.recv(self.BUFFER)
            except Exception as e:
                self.messenger.add_error("Could not receive heartbeat from auth peer: " + str(e))
                self.leave()
            try:
                self.auth_socket.send(send_json({"<3": True}))
            except Exception as e:
                self.messenger.add_error("Could not send heartbeat to auth peer: " + str(e))
                self.leave()
                return

            time.sleep(2)
