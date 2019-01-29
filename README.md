# netw0rk

## Protocol Outline
#### Participants
Peers   (Raspberry Pi's w/ WiFi and Bluetooth)
Clients (smartphones via app)

#### Parameters
T = client authentication time interval (say 24 hours)
n = the number of peers a client needs to receive authentications from

### Bluetooth Authentication Specification
1. Establish Connection via BLE
  - RESEARCH: range of BLE and whether information can be transmitted without forming a connection (via changing the device name)
2. Peer produces a signature: Sign(PeerID || ClientID || Date) and transmits it back to the client. 
3. Client collects n such signatures from peers.
4. Upon getting S = \[S1,S2,...,Sn] such signatures, the client sends S (SigSet) to the last signing peer. 
5. The Peer verifies the signature set as follows:
  - If the hash of the sorted PeerID list (P = \[P1, P2,...Pn]) exists in SigSet table, do nothing.
  - Else: Produce a signature, $i for the SigSet, 
  - Directly send SigSet + $i + (all other received $'s) to a peer p ∈ P which can be immediately connected with, and who has not yet signed the SigSet
    - RESEARCH: How to efficiently 'directly' connect with a peer (socketing?)
  - If len() >= S, transmit SigSet + $ to authenticating client. cannot find a direct peer ∈ P, drop SigSet.
  - 
  #### SigSet Table
  | ClientID        | Timestamp     | SigSet Peer Hash  |
  | --------------- |:-------------:| -----------------:|
  | 1234            | 1548718597    | afh13roidn9       |
  | 5678            | 1548703652    | grepk1239fnz      |
    * After time period



## Resources
https://www.ralfebert.de/ios/tutorials/multipeer-connectivity/

https://www.bluetooth.com/bluetooth-technology/topology-options/le-mesh/mesh-tech

https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/NetServices/Introduction.html

http://zeromq.org/bindings:swift-binding

https://github.com/ethereum/devp2p/blob/master/rlpx.md

https://developer.apple.com/documentation/networkextension/nehotspothelper
