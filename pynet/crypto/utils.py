"""
BLS Crypto toolkit.
All input and output of below functions is in bytes.
Using BLSPY by Chia Network
@YCRYPTX
"""

import os.path as path
from blspy import (PrivateKey, PublicKey,
                   Signature, AggregationInfo,
                   ExtendedPrivateKey, BLS)

KEY_FILE_PATH =  path.abspath(path.join(__file__ ,"../../local/bls_sk"))

def seed_gen():
    import os
    return os.urandom(32)

# Creates new BLS-compatible private key from a random seed
# saves it in serialized form to ../local/bls_sk
def private_key_gen(seed = None):
    if seed == None:
        sk = PrivateKey.from_seed(seed_gen())
    else:
        sk = PrivateKey.from_seed(seed)
    sk_bytes = sk.serialize()
    output_file = open(KEY_FILE_PATH, "wb")
    output_file.write(sk_bytes)
    output_file.close()
    return sk_bytes

def get_pub_key():
    sk_bytes = open(KEY_FILE_PATH,"rb").read()
    sk = PrivateKey.from_bytes(sk_bytes)
    return sk.get_public_key().serialize()


def sign(msg):
    sk_bytes = open(KEY_FILE_PATH,"rb").read()
    sk = PrivateKey.from_bytes(sk_bytes)
    return sk.sign(msg).serialize()

def verify_sig(msg, _pub_key, _sig):
    sig = Signature.from_bytes(_sig)
    pub_key = PublicKey.from_bytes(_pub_key)
    sig.set_aggregation_info(AggregationInfo.from_msg(pub_key, msg))
    ok = sig.verify()
    return ok


# Accepts [<Signature types>]
def group_sign(sigs):
    # sigs = list(map(lambda x: Signature.from_bytes(x), _sigs))
    return Signature.aggregate(sigs).serialize()


def aggregate_pub_keys(_keys):
    keys = list(map(lambda x: PublicKey.from_bytes(x), _keys))
    return PublicKey.aggregate(keys).serialize()

def sigs_deseriazlize(_sigs):
    return list(map(lambda x: Signature.from_bytes(x), _sigs))
