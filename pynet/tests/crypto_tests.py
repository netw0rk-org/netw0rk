from context import utils
from context import formatting
from blspy import (PrivateKey, PublicKey,
                   Signature, AggregationInfo,
                   ExtendedPrivateKey, BLS)


_seed = bytes([0, 50, 6, 244, 24, 199, 1, 25, 52, 88, 192,
                19, 18, 12, 89, 6, 220, 18, 102, 58, 209,
                82, 12, 62, 89, 110, 182, 9, 44, 20, 254, 22])
_sk = PrivateKey.from_seed(_seed)
_pk = _sk.get_public_key()

_msg = bytes([100, 2, 254, 88, 90, 45, 23])

_sig = _sk.sign(_msg)

# Not a great test
def t_seed_gen():
    s1 = utils.seed_gen()
    s2 = utils.seed_gen()
    s3 = utils.seed_gen()

    assert (not (s1 == s2 or s1 == s3 or s2 == s3)), "Seed_gen() is totally not random"



def t_private_key_gen():
    assert utils.private_key_gen(), "failed to gen priv key :without provided seed:"
    assert _sk == PrivateKey.from_bytes(utils.private_key_gen(_seed)), "gerating private key wrongly"

def t_get_pub_key():
    utils.private_key_gen(_seed) #set priv key to example one
    pubkey = utils.get_pub_key()
    assert PublicKey.from_bytes(pubkey) == _pk, "Not retrieving public key properly, perhaps priv key is wrong"

#TODO: Unimplemented
def t_sign():
    msg = "MargaretThatcher69"
    bmsg = formatting.binary_string([msg])
    utils.private_key_gen(_seed)
    assert utils.sign(bmsg), "signing fails"

def t_verify():
    msg = "MargaretThatcher69"
    bmsg = formatting.binary_string([msg])
    utils.private_key_gen(_seed)
    sig = utils.sign(bmsg)
    pubkey = utils.get_pub_key()
    assert utils.verify_sig(bmsg, pubkey, sig), "Signature verification fails"
    try:
        assert utils.verify_sig(bmsg +b'\x00', pubkey, sig), ""
        assert False, "signature verification does not fail on bad sig"
    except Exception as e:
        True
        
def t_group_sign_verify():
    msg = "NSAWatches"
    bmsg = formatting.binary_string([msg])
    privates = [utils.private_key_gen() for i in range(5)]
    publics = [PrivateKey.from_bytes(i).get_public_key().serialize() for i in privates]
    sigs = [PrivateKey.from_bytes(i).sign(bmsg) for i in privates]
    assert utils.group_sign(sigs), "failing on group_sign()"
    group_sig = utils.group_sign(sigs)
    assert utils.aggregate_pub_keys(publics), "failing on aggregate_pub_keys()"
    agg_key = utils.aggregate_pub_keys(publics)
    assert utils.verify_sig(bmsg, agg_key, group_sig), "aggregate sig verification fails"

    # sigs_s = [PrivateKey.from_bytes(i).sign(bmsg).serialize() for i in privates]
    # sigs_s_1 = [i.serialize() for i in sigs]
    # for i in range(len(sigs_s)):
    #     assert sigs_s[i] == sigs_s_1[i], "mismatch on serialized, item {}".format(i)
    # sigs_s_deser = [Signature.from_bytes(i) for i in sigs_s]
    # for i in range(len(sigs)):
    #     assert sigs_s_deser[i] == sigs[i], "mismatch on deserialized, item {}".format(i)

# msg = b'NSAWatches'
# privates = [PrivateKey.from_seed(_seed).serialize() for i in range(5)]
# publics = [PrivateKey.from_bytes(i).get_public_key().serialize() for i in privates]
# sigs = [PrivateKey.from_bytes(i).sign(msg).serialize() for i in privates]
# _sigs = [Signature.from_bytes(i) for i in sigs]
# assert Signature.aggregate(_sigs), "failing on group_sign()"



t_seed_gen()
t_private_key_gen()
t_get_pub_key()
t_sign()
t_verify()
t_group_sign_verify()
