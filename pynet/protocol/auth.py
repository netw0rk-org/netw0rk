"""
Authentication helper functions
@YCRYPTX
"""
from context import utils, formatting
from . import params
from functools import reduce
import time

def _sstable_set_check(S):
    #perform the SigSet check
    return True

def _peer_table_check(S):
    #
    return True

def _verify_sigs(sigs, pubkeys, msgs):
    # verify each signature in S to be valid, and from a known peer (in Peer_Table)
    # and with timestamp less than T_interval
    _peer_table_check(pubkeys)
    for i in range(len(sigs)):
        if not utils.verify_sig(msgs[i], pubkeys[i], sigs[i]):
            raise ValueError("1 or more peer signatures is flawed")
    return True

#validates that all messages are properly formatted [ClientPubKey '\x00' Timestamp]
#returns the clientpubkey, minimum timestamp
def _validate_msgs(msgs):
    if len(msgs[0]) != 2:
        raise ValueError("1 or more peer signatures is flawed")
    client_pub_key = msgs[0][0]
    try:
        max_timestamp = formatting.int_ts(msgs[0][1])
        min_timestamp = formatting.int_ts(msgs[0][1])
    except:
        raise ValueError("1 or more messages include an invalid timestamp")
    for m in msgs:
        if len(m) != 2:
            raise ValueError("1 or more peer signatures is flawed")
        if client_pub_key != m[0]:
            raise ValueError("Signature set includes more than 1 client public key")
        try:
            m_ts = formatting.int_ts(m[1])
        except:
            raise ValueError("1 or more messages include an invalid timestamp")
        if m_ts > max_timestamp:
            max_timestamp = m_ts
        if m_ts < min_timestamp:
            min_timestamp = m_ts
        client_pub_key = m[0]

    if max_timestamp - min_timestamp > params.T_INTERVAL:
        raise ValueError("Signature set time interval is too long")
    return client_pub_key, min_timestamp

#returns the pubkey list in bytes sorted by timestamp
def _sort_pub_keys(timestamps, pubkeys):
    linker = dict(zip(timestamps, pubkeys))
    timestamps.sort()
    return [linker[i] for i in timestamps]

# finds the timestamp in the to_sign  sig set byte object
def extract_ts(to_sign):
    r = len(to_sign) % params.PUB_LEN
    return to_sign[-r:]

# finds the public keys of peers in to_sign sig set byte object
def extract_peer_keys(to_sign):
    r = len(to_sign) % params.PUB_LEN
    return to_sign[params.PUB_LEN:len(to_sign) - r]

# caller function records all other SigSets and if SigSet == n
# create the BLS group signature and broadcast to the client
# Max # of signatures is set to params.MAX_SIGS, for now!
# If len(S) > N then as the earliest signature pick S_sorted_by_date[len(S) - N]
def sign_sigset(_sigs, _pub_keys, _msgs):
    if not (len(_sigs) == len(_pub_keys) == len(_msgs) and len(_sigs) < params.MAX_SIGS and len(_sigs) > 0):
        raise ValueError("Non-compatible size of signature set data")
    msgs = [[i[:params.PUB_LEN],i[params.PUB_LEN:]] for i in _msgs]
    client_pub_key, min_timestamp = _validate_msgs(msgs)
    sigs = utils.sigs_deseriazlize(_sigs)
    pub_keys = utils.pub_keys_deseriazlize(_pub_keys)
    _sstable_set_check(sigs)
    _verify_sigs(_sigs, _pub_keys, _msgs)
    # pub keys sorted by timestamp and concatenated
    p = reduce(lambda x, y: x + y , _sort_pub_keys([formatting.int_ts(i[1]) for i in msgs], _pub_keys))
    to_sign = client_pub_key + p + formatting.timestamp(min_timestamp)
    return utils.sign(to_sign), to_sign




#NOTE:  if a user provides an earlier signature it must be included as timestamp
#TODO:  A wrapper function where this method is called from, that checks if
#       user had already been signed by a peer AND checks if that peer is known (peer_table)
def sign_user(client_pub_key, timestamp = None):
    ts = timestamp if timestamp else time.time()
    ts_sanitized = formatting.timestamp(ts)
    to_sign = client_pub_key + ts_sanitized
    return utils.sign(to_sign)
