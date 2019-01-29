# netw0rk

## Protocol Outline
#### Participants
Peers   (Raspberry Pi's w/ WiFi and Bluetooth)
Clients (smartphones via app)

#### Parameters
T = client authentication time interval (say 24 hours)
n = the number of peers a client needs to receive authentications from

### Bluetooth Authentication 
1. Establish Connection via BLE
    - *Research: range of BLE and whether information can be transmitted without forming a connection (via changing the device name)*
2. Peer produces a signature: Sign(PeerID || ClientID || Date) and transmits it back to the client. 
3. Client collects n such signatures from peers.
4. Upon getting S = \[S1,S2,...,Sn] such signatures, the client sends S (SigSet) to the last signing peer. 
5. Peers verify the signature set as follows:
    - If the hash of the sorted PeerID list (P = \[P1, P2,...Pn]) exists in SigSet Table, do nothing.
    - Else: Produce a signature, Ši, for the SigSet. Š = Ši + all other received SigSet signatures
    - If len(Š) < S, directly send SigSet + Š to a peer p ∈ P which can be immediately connected with, and whose sig ∉ Š. If such a peer cannot be found, drop SigSet + Š.
      - *Research: How to efficiently 'directly' connect with a peer (socketing?)*
    - Else: Send SigSet + Š to authenticating client. 
  #### SigSet Table
  | ClientID        | Timestamp     | SigSet Peer Hash  |
  | --------------- |:-------------:| -----------------:|
  | 1234            | 1548718597    | afh13roidn9       |
  | 5678            | 1548703652    | grepk1239fnz      |
  
  Remove row_i from table if current_timestamp - timestamp_i > n





## Resources
https://www.ralfebert.de/ios/tutorials/multipeer-connectivity/

https://www.bluetooth.com/bluetooth-technology/topology-options/le-mesh/mesh-tech

https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/NetServices/Introduction.html

http://zeromq.org/bindings:swift-binding

https://github.com/ethereum/devp2p/blob/master/rlpx.md

https://developer.apple.com/documentation/networkextension/nehotspothelper
