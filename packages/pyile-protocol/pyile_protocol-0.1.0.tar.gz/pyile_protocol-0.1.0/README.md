<h1 style="text-align:center;">Pyile Protocol Documentation:</h1>
<h2>Introduction:</h2>
<p>
This document describes the network protocol used by the Pyile application over TCP/IP on port 4702. 
The protocol is used for communication and authentication between peers. 
</p>

<h2>Protocol Overview</h2>
<p>
The Pyile protocol is used for peer-to-peer communication and authentication. This protocol allows for a single central 
authenticator that established the network and is the source of all authentication within the given network. With this in mind,
the authenticating peer has a unique role. It is still considered a peer which means that they still have full communication
functionalities. The Pyile protocol supports another type of peer which is a <i>non-authenticating</i> peer or just <i>peer</i>.
This type of peer only can be authenticated and send messages.
</p>

<h4>Sockets:</h4>
<ul>
    <li><b>Port 4702</b>: Used as the main connection between peer and authenticating peer.</li>
    <li><b>Dynamic and private port</b>: Randomly generated port that is within the private use range. Used for communication between
    all peers.</li>
    <li>
    <b>Temporary Socket</b>: Used to send messages and broadcast but is then closed immediately after.
    </li>
</ul>


<h3>Protocol Flow</h3>

* Authenticating peer is established listening on port 4702 for potential peers
* Authenticating peer, then generates a random port and begins to listen to already established peers. (Should only be themselves)
* A Joining peer then requests to be authenticated by the initial peer.
* The initial peer then checks if the peer is already banned and then checks the password.
* If the password is correct, then the peer is added and then given the list of peers that can be communicated with.
* A heartbeat is then established between both peers.
* The joining peer can now communicate in the network through broadcasting or individual messaging.

<h3>Special Flows</h3>

<h4>Heartbeat</h4>

* When a peer is authenticated, A heartbeat is established between the authenticating peer and peer.
* The peer is in a constant state of listening, waiting to send a response to the authenticating peer.
* If a timeout is reached on either sides, the peer will be removed from the list of established peers and must reauthenticate.

<h4>Exit</h4>

* Any time an exit is called by a peer, the instance variable <i>disconnected</i> will be set to True. All sockets will be closed and any loose threads will be joined.

<div></div>
<img src="https://github.com/nburnet1/nburnet1.github.io/blob/main/public/Pyile.png"/>
<h5><i>Figure 1</i></h5>

<h3>Message Types</h3>

* Banned status - First message sent to peer from authenticating peer. if banned, connection with joining peer is dropped
* Authenticated - Second message sent from authenticating peer. If authenticated, a heartbeat is established
* Heartbeat - Sent throughout the life of the connection that ensures both peers are still alive.
* Set Distributions - When the Authenticating peer has made changes to the peer list, it redistributes to all the peers in the network.
* Communication - Simple messaging between peers

<h3>Error Handling</h3>
<p>
The protocol has custom exceptions to further the detail of errors:
</p>
<ul>
    <li><i>AuthenticationException</i></li>
    <li><i>StatusException</i></li>
    <li><i>SendException</i></li>
    <li><i>RecvException</i></li>
</ul>


<h3>Security</h3>
<p>
The protocol implements an authentication process equipped with a password check and banned status. At this time, there is no encryption.
</p>

<h2>Code Example</h2>

<h4>Install</h4>

```
pip install pyile_protocol
```

<h4>Authenticating Peer</h4>

```python
import threading
from pyile_protocol.lib.peers.AuthPeer import AuthPeer

auth_peer = AuthPeer(address=("192.168.1.66", 4702), password_attempts=1, password="password")

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
    else:
        auth_peer.broadcast(data)
```
<h4>Peer</h4>

```python
import threading
from pyile_protocol.lib.peers.JoinPeer import JoinPeer
peer = JoinPeer(address=("192.168.1.65", 4702))
peer.get_authenticated(("192.168.1.66", 4702), "password")


connect_thread = threading.Thread(target=peer.connect)
connect_thread.start()


while not peer.disconnected:
    data = input("~: ")
    if data == "exit":
        peer.leave()

    elif data == "peers":
        print(peer.peers)
    else:
        peer.broadcast(data)
```
