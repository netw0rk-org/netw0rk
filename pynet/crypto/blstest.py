# import bls.scheme as bls
#
# m = [3] * 2 # messages
# n = 3 # number of authorities
# params = bls.setup()
# print("\nsetup", params)
#
# # generate key
# (sk, vk) = bls.ttp_keygen(params, n, n)
# print("\n\nsk",sk)
# print("\n\nvk",vk)


from blspy import (PrivateKey, PublicKey,
                   Signature, AggregationInfo,
                   ExtendedPrivateKey, BLS)

seed = bytes([0, 50, 6, 244, 24, 199, 1, 25, 52, 88, 192,
                19, 18, 12, 89, 6, 220, 18, 102, 58, 209,
                82, 12, 62, 89, 110, 182, 9, 44, 20, 254, 22])
sk = PrivateKey.from_seed(seed)
pk = sk.get_public_key()

msg = bytes([100, 2, 254, 88, 90, 45, 23])

sig = sk.sign(msg)
