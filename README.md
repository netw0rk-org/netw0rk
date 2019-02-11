# netw0rk

## Protocol Outline
### Participants
- Peers   (Raspberry Pi's w/ WiFi and Bluetooth)
- Clients (smartphones via app)

### Parameters
- T_interval = client authentication time interval (say 24 hours)
- T_sigset = The time interval after which a client can reuse the same signature set (say 48 hours)
- T_inter = The max time interval after which a peer can sign on a previously provided timestamp (say 15 minutes) [described in Bluetooth Authentication step 5]
- n = the number of peers a client needs to receive authentications from

### Bluetooth Authentication
1. Client establishes connection to a peer via BLE
2. Peer produces a signature: Sign( ClientPubKey || timestamp ) and transmits it back to the client.
3. Client collects n such signatures from n peers.
4. Upon getting S = \[S1,S2,...,Sn] such signatures, the client sends S (SigSet) to the last signing peer.
5. Peers form signature set as follows:
    - If the hash, H, of the sorted PeerID list (P = \[P1, P2,...Pn]) exists in SigSet Table, do nothing.
    - Verify each signature in the set (is valid sig, and belongs to a peer, p ∈ peer_table)
    - Verify that max_timestamp(S) - min_timestamp(S) < T_inter
    - Concatenate P || ClientPubKey || min_timestamp(S), and sign (call it Ši).
    - Add client_pub_key, current_timestamp, and H to SigSet_Table
    - Send Ši and S to all peers in S.
    - After receiving Ši,..., Šn signatures, a peer forms a BLS group signature Š using Ši,..., Šn, and sends Š to client


 #### SigSet_Table
  | ClientPubKey    | Timestamp     | SigSet Peer Hash  |
  | --------------- |:-------------:| -----------------:|
  | 1234            | 1548718597    | afh13roidn9       |
  | 5678            | 1548703652    | grepk1239fnz      |

    - Remove row_i from table if current_timestamp - timestamp_i > n

### Mesh Networking

#### Forwarding
- ~~Packets are only forwarded if BT Auth is valid.~~ Inter-peer communication is unrestricted, that is, peers can forward packets between each other without performing any signature validation.
- Entry and Exit peers (the peer who first receives a packet from a client, and the peer who forwards the packet to its destination), are the only ones who perform authentication verification. This includes:
    - BT Auth verification, once per session.
    - Client Signature verification on every packet
- A valid BT Auth:
    - for s ∈ SigSet, packet_userid == s(sigset_userid)
    - is a SigSet which is itself signed by all signing peers.
    - has current_timestamp - min_timestamp(SigSet) < n. min_timestamp is the timestamp of the oldest signature ∈ SigSet
    - for s ∈ SigSet, s(PeerID) ∈ Peer_Table, and s is a valid signature for PeerID
- *Research: can the BT Auth be made smaller? SigSet + Š seems quite big*
- Use CJDNS for forwarding?


#### Peering
-

#### Peer_Table
  | Peer Public Key |
  | --------------- |
  | xzalskd-0       |
  | zxqwfpo-2       |







## Resources
https://www.ralfebert.de/ios/tutorials/multipeer-connectivity/

https://www.bluetooth.com/bluetooth-technology/topology-options/le-mesh/mesh-tech

https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/NetServices/Introduction.html

http://zeromq.org/bindings:swift-binding

https://github.com/ethereum/devp2p/blob/master/rlpx.md

https://developer.apple.com/documentation/networkextension/nehotspothelper

https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html

https://github.com/asonnino/bls

https://github.com/warner/python-ecdsa
