from context import auth, formatting, utils
import time
from blspy import Signature, PrivateKey

def t_sign_user():
    client = "snowden123"
    ts = 1234.1234
    assert auth.sign_user(client, ts), "failed to sign user with provided timestamp"
    assert auth.sign_user(client), "failed to sign user without timestamp"

def t_sign_sigset():
    msg = "watching_us"
    bmsg = formatting.binary_string([msg])
    privates = [utils.private_key_gen() for i in range(5)]
    publics = [PrivateKey.from_bytes(i).get_public_key().serialize() for i in privates]
    sigs = [PrivateKey.from_bytes(i).sign(bmsg) for i in privates]
    assert auth.sign_sigset(sigs), "failed to sign sigset"



t_sign_user()
t_sign_sigset()
