import utils
import time

def sstable_set_check(S):
    #perform the SigSet check
    return True

def sstable_date_check(client_pub_key):
    # perform the client date check
    return True

# TODO: Use BLS group signature
def sign_sigset(S):
    if sstable_set_check(S):
        return utils.signer(s)

# timestamp must be False if the user provides an earlier signature
def sign_user(client_pub_key, timestamp):
    #
    if sstable_date_check(client_pub_key):
        ts = timestamp if timestamp else time.time()
        to_sign = [client_pub_key, "{}".format(ts)]
        return utils.signer(to_sign)
    else:
        return False, False
