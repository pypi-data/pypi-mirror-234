import threading

from pyile_protocol.lib.peers.AuthPeer import AuthPeer
from pyile_protocol.lib.messenger.Messenger import Messenger


def test_auth():
    messenger = Messenger()
    auth_peer = AuthPeer(address=("172.20.101.26", 4702), password_attempts=2, password="password", messenger=messenger,
                         alias="admin")
    # auth_peer = AuthPeer(("172.20.100.39", 4702), 1, "password")
    print(auth_peer)

    auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
    peer_thread = threading.Thread(target=auth_peer.connect)
    auth_thread.start()
    peer_thread.start()

    while not auth_peer.disconnected:
        data = input("~: ")
        if data == "exit":
            auth_peer.leave()
        elif data == "peers":
            print(auth_peer.peers)
        elif data == "auth":
            print(auth_peer.connected_addrs)
        elif data == "dist":
            print(auth_peer.dist_sockets)
        elif data == "threads":
            print(threading.active_count())
        elif data == "check":
            print(messenger.get_messages())
        elif data == "limbo":
            print(auth_peer.limbo_peers)
        elif data == "banned":
            print(auth_peer.blocked_peers)
        elif data == "log":
            print(auth_peer.messenger.seq_list)
        elif "send:" in data:
            data = data.split(":")
            print(data)
            print(tuple((data[2], int(data[3]))))
            auth_peer.send(tuple((data[2], int(data[3]))), data[1], tuple((data[2], int(data[3]))))
        else:
            auth_peer.broadcast(data)
