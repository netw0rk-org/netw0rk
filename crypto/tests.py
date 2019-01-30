import utils

utils.generate_secret()
to_sign = ["carlos","is","a","person"]
sig = utils.signer(to_sign)
print(sig, to_sign)
utils.verify_sig(sig, to_sign)
