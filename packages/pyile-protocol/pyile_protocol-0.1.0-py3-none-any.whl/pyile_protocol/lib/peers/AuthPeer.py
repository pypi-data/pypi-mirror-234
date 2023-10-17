import threading
import time

from pyile_protocol.lib.peers.Peer import Peer
from pyile_protocol.lib.utils import *
from pyile_protocol.lib.error import *


class AuthPeer(Peer):
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------

    address : tuple of (ip, port)
        address of the authentication peer
    password_attempts : int
        Allowed attempts that a joining peer is allowed
    password : str
        Password that joining peers must authenticate with
    blocked_peers : set
        Set of peers that are banned from joining the network
    changes_made : bool
        Boolean to check if changes have been made to the network


    Methods
    -------
    __init__(address, password_attempts, password)
        Constructor for the AuthPeer class
    authenticate_peers()
        The first method that should be called when an authentication peer is created
    """

    def __init__(self, address, password_attempts, password, messenger, alias):
        Peer.__init__(self, address=address, messenger=messenger, alias=alias)
        self.password_attempts = password_attempts
        self.peers.append(self.peer_address)
        self.blocked_peers = set()
        self.changes_made = False
        self.password = password
        self.connected_addrs = []
        self.limbo_peers = {}
        self.dist_sockets = []

    def _auth_password_check(self, addr):
        """
            Auxiliary function to help authenticate
        :return: peer_address if authenticated, None if not
        """
        try:
            password = addr.recv(self.BUFFER)
            password_json = recv_json(password)
            self.messenger.add_info(str(addr.getpeername()) + " is trying to login.")
            if password_json["shadow"] == self.password:
                # Sends authenticated status to peer
                auth = send_json({"authenticated": True})
                addr.send(auth)
                # Receives peer_address from peer
                peer_recv = addr.recv(self.BUFFER)
                peer_json = recv_json(peer_recv)
                peer_tuple = tuple(peer_json["peer_address"])
                self.peers.append(peer_tuple)
                # Sends new set to peer
                distro_json = send_json({"distro": self.peers})
                addr.send(distro_json)
                return peer_tuple
            else:
                auth = send_json({"authenticated": False})
                wrong_pw_addr = addr.getpeername()[0]
                if wrong_pw_addr in self.limbo_peers:
                    self.limbo_peers[wrong_pw_addr] += 1
                    if self.limbo_peers[wrong_pw_addr] >= self.password_attempts:
                        self.blocked_peers.add(wrong_pw_addr)
                        self.limbo_peers.pop(wrong_pw_addr)
                else:
                    self.limbo_peers[wrong_pw_addr] = 1

                addr.send(auth)
                raise AuthenticationException(str(addr.getpeername()) + "entered the incorrect password.")
        except AuthenticationException as e:
            self.messenger.add_info(str(e))
            return None

    def authenticate_peers(self):
        """
        The first method that should be called when an authentication peer is created.
        Starts a thread to listen for incoming connections, Authenticates peers and calls the
        heartbeat method.
        """
        distribute_thread = threading.Thread(target=self.auth_distribute)
        self.dist_socket.listen()
        distribute_thread.start()

        self.auth_socket.listen()

        while not self.disconnected:
            try:
                addr, acc_connect = self.auth_socket.accept()
                self.messenger.add_info("Got connection from: " + str(addr.getpeername()))
                # self.blocked_peers.add(addr.getpeername())  # Uncomment to test ban.
                # Checks if joining peer in banned
                if addr.getpeername()[0] not in self.blocked_peers:
                    # Sends not banned status to peer
                    try:
                        banned = send_json({"banned": False})
                        addr.send(banned)
                        self.messenger.add_info("Sent Banned status: " + str(recv_json(banned)))
                    except AuthenticationException:
                        self.messenger.add_error("Could not send banned status to peer.")
                    # Performs authentication
                    peer_address = self._auth_password_check(addr)
                    if peer_address is not None:
                        if peer_address[0] in self.limbo_peers:
                            self.limbo_peers.pop(peer_address[0])
                        addr.send(send_json({"dist_addr": self.dist_address}))
                        dist_connected = self.dist_socket.accept()
                        self.dist_sockets.append(dist_connected)
                        self.messenger.add_info("added dist address " + str(dist_connected))
                        self.connected_addrs.append(addr)
                        auth_thread = threading.Thread(target=self.auth_beat, args=(addr, peer_address, dist_connected))
                        auth_thread.start()
                        self.changes_made = True

                else:
                    self.messenger.add_info(str(addr.getpeername()) + "is banned")
                    banned = send_json({"banned": True})
                    addr.send(banned)
                    addr.close()
            except:
                pass

    def auth_beat(self, addr, peer_address, dist_addr):
        """
        Sends a heartbeat to the peer to check if it is still connected
        :return:
        """
        while not self.disconnected:
            try:
                addr.send(send_json({"<3": True}))
                beat = addr.recv(self.BUFFER)
                if not beat:
                    raise ConnectionResetError
            except ConnectionResetError:
                self.messenger.add_info("Peer disconnected: " + str(peer_address))
                self.peers.remove(peer_address)
                self.connected_addrs.remove(addr)
                self.dist_sockets.remove(dist_addr)
                self.changes_made = True
                return
            time.sleep(2)

    def auth_distribute(self):
        while not self.disconnected:
            if self.changes_made and len(self.dist_sockets) > 0:
                for addr in self.dist_sockets:
                    distro_json = send_json({"distro": self.peers})
                    addr[0].send(distro_json)
                self.changes_made = False
