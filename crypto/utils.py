from ecdsa import SigningKey
import time


# Not Secure... DER shouldn't be stored in the /crypto directory
def generate_secret():
    sk = SigningKey.generate() # uses NIST192p
    der = sk.to_der()
    output_file = open("signing_key.der", "wb")
    output_file.write(der)
    output_file.close()
    return 0

def get_signing_key():
    sk_der = open("signing_key.der","rb").read()
    sk = SigningKey.from_der(sk_der)
    return sk

def sign(user_pub_key):
    timestamp = time.time()
    sk = get_signing_key()

    signature = sk.sign_deterministic(b"{}{}".format(user_pub_key, timestamp))
    return signature, user_pub_key, timestamp

def verify_sig(sig, content):
    sk = get_signing_key()
    vk = sk.get_verifying_key()
    assert vk.verify(sig, content)
    return True

# generate_secret()
# sig, user, t = sign("carlos")
# print(sig, t)
# verify_sig(sig, b"{}{}".format(user, t))
