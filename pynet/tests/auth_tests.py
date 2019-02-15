from context import auth, formatting, utils, params
import time
from blspy import Signature, PrivateKey
from functools import reduce

def t_sign_user():
    client = PrivateKey.from_bytes(utils.private_key_gen()).get_public_key().serialize()
    ts = 1234.1234
    assert auth.sign_user(client, ts), "failed to sign user with provided timestamp"
    assert auth.sign_user(client), "failed to sign user without timestamp"

def t_sign_sigset():
    pubkey = PrivateKey.from_bytes(utils.private_key_gen()).get_public_key().serialize()
    msgs = []
    for i in range(3):
        time.sleep(1)
        msgs.append(pubkey + formatting.timestamp(time.time()))
    privates = [utils.private_key_gen() for i in range(3)]
    publics = [PrivateKey.from_bytes(i).get_public_key().serialize() for i in privates]
    sigs = [PrivateKey.from_bytes(i).sign(msgs[privates.index(i)]).serialize() for i in privates]

    #check correct error raising when input is bad
    try:
        auth.sign_sigset([],[],[])
        assert False, 'failed to throw exception of empty signatures'
    except ValueError as e:
        True
    try:
        auth.sign_sigset([0 for i in range(51)],[0 for i in range(51)],[0 for i in range(51)])
        assert False, 'failed to throw exception of greater than 50 signatures'
    except ValueError as e:
        True
    try:
        auth.sign_sigset([0 for i in range(5)], [0 for i in range(10)], [0 for i in range(5)])
        assert False, 'failed to throw exception of not same length inputs'
    except ValueError as e:
        True
    try:
        bad_msgs = list(msgs)
        bad_msgs[1] = b'not a pubkey + nullbyte + timestamp'
        auth.sign_sigset(sigs, publics, bad_msgs)
        assert False, 'failed to throw exception of bad messages (not pubkey + timestamp)'
    except ValueError as e:
        True
    try:
        bad_msgs = list(msgs)
        bad_msgs[2] = b'not a pubkey + nullbyte + timestamp'
        auth.sign_sigset(sigs, publics, bad_msgs)
        assert False, 'failed to throw exception of bad messages (not pubkey + timestamp)'
    except ValueError as e:
        True
    try:
        bad_msgs = list(msgs)
        bad_msgs[0] = b'not a pubkey + nullbyte + timestamp'
        auth.sign_sigset(sigs, publics, bad_msgs)
        assert False, 'failed to throw exception of bad messages (not pubkey + timestamp)'
    except ValueError as e:
        True
    try:
        bad_msgs = list(msgs)
        bad_msgs[2] = b'different_pub_key' + bad_msgs[2][params.PUB_LEN:]
        auth.sign_sigset(sigs, publics, bad_msgs)
        assert False, 'failed to throw exception because more than 1 client pub key'
    except ValueError as e:
        True
    try:
        bad_msgs = list(msgs)
        bad_msgs[2] = bad_msgs[2][:params.PUB_LEN] + b'this aint a timestamp!'
        auth.sign_sigset(sigs, publics, bad_msgs)
        assert False, 'failed to throw exception because of a non-valid timestamp'
    except ValueError as e:
        True

    # test min_timestamp calculation
    ts_msgs = list(reversed(msgs))
    ts_sigs = [PrivateKey.from_bytes(i).sign(ts_msgs[privates.index(i)]).serialize() for i in privates]
    _, to_sign  = auth.sign_sigset(ts_sigs, publics, ts_msgs)
    min_ts = formatting.timestamp(msgs[0][params.PUB_LEN:])
    to_sign_ts = auth.extract_ts(to_sign)
    assert min_ts == to_sign_ts, "fails to pick the minimum timestamp and sign it"

    # test correct sorting of public keys
    r_publics = list(reversed(publics))
    to_sign_publics = auth.extract_peer_keys(to_sign)
    r_publics_reduced = reduce(lambda x, y: x + y, r_publics)

    assert r_publics_reduced == to_sign_publics , "fails to properly sort the set of peer public keys by timestamp "

    # test signature validation
    try:
        bad_sigs = list(sigs)
        bad_sigs[1] = bad_sigs[0]
        auth.sign_sigset(bad_sigs, publics, msgs)
        assert False, "failed to catch a bad signature (1)"
    except ValueError as e:
        True
    try:
        bad_sigs = list(sigs)
        bad_sigs[1] = b'x\01010101'
        auth.sign_sigset(bad_sigs, publics, msgs)
        assert False, "failed to catch a bad signature (2)"
    except ValueError as e:
        True


    assert auth.sign_sigset(sigs, publics, msgs), "failed to sign sigset"
    print("sigset passes")



t_sign_user()
t_sign_sigset()
