from context import utils, formatting
import time

def sstable_set_check(S):
    #perform the SigSet check
    return True


# TODO: Use BLS group signature
def sign_sigset(sigs):
    if sstable_set_check(sigs):
        # sigs = utils.sig_deseriazlize(_sigs)
        sigset = utils.group_sign(sigs)
    else:
        raise ValueError("Client trying to repeat SigSet")



#NOTE:  if a user provides an earlier signature it must be included as timestamp
#TODO:  A wrapper function where this method is called from, that checks if
#       user had already been signed by a peer AND checks if that peer is known (peer_table)
def sign_user(client_pub_key, timestamp = None):
    ts = timestamp if timestamp else time.time()
    to_sign = [client_pub_key, str(timestamp)]
    _to_sign = formatting.binary_string(to_sign)
    return utils.sign(_to_sign)
