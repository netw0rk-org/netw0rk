import utils
import time

def sstable_set_check(S):
    #perform the SigSet check
    return True


# TODO: Use BLS group signature
def sign_sigset(S):
    if sstable_set_check(S):
        return utils.signer(s)
    else:
        raise ValueError("Client trying to repeat SigSet")



#NOTE:  timestamp must be False if the user provides an earlier signature
#TODO:  A wrapper function where this method is called from, that checks if
#       user had already been signed by a peer AND checks if that peer is known (peer_table)
def sign_user(client_pub_key, timestamp):
    #
    ts = timestamp if timestamp else time.time()
    to_sign = [client_pub_key, "{}".format(ts)]
    return utils.signer(to_sign), to_sign
