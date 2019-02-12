"""
Authentication helper functions
 - We need message ID's
    1. Signature set formation request from client
    2. Signature set formation from peer
    3. BT Signture to client
    4. Signature set from peer to client
- Need to standardize timestamps (convert to int?) and delimit each phrase in
the concatenation (of timestamp, pubkeys, etc. )
- Create a makefile!!! 
@YCRYPTX
"""
from context import utils, formatting
import time

def sstable_set_check(S):
    #perform the SigSet check
    return True

def verify_sigs(S):
    # verify each signature in S to be valid, and from a known peer (in Peer_Table)
    return True

def verify_timestamp(S):
    # Verify that max_timestamp(S) - min_timestamp(S) < T_inter
    # If len(S) > N then as the earliest signature pick S[len(S) - N]
    return True

def sign_sigset(_sigs, msg, ):
    sigs = utils.sigs_deseriazlize(_sigs)

    assert sstable_set_check(sigs), "Client trying to repeat SigSet"
    assert verify_sigs(sigs), "A signature in the provided set is invalid"
    assert verify_timestamp(sigs), "Too much time elapsed between the provided signatures"
    # Concatenate P (ascendingly sorted PeerID list (P = [P1, P2,...Pn])) || ClientPubKey || min_timestamp(S)
    return utils.group_sign(sigs)




#NOTE:  if a user provides an earlier signature it must be included as timestamp
#TODO:  A wrapper function where this method is called from, that checks if
#       user had already been signed by a peer AND checks if that peer is known (peer_table)
def sign_user(client_pub_key, timestamp = None):
    ts = timestamp if timestamp else time.time()
    to_sign = [client_pub_key, str(timestamp)]
    _to_sign = formatting.binary_string(to_sign)
    return utils.sign(_to_sign)
