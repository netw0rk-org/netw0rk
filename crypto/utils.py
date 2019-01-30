from ecdsa import SigningKey
import formatting

# NOTE: Not Secure... DER shouldn't be stored in the /crypto directory
#
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


# TODO: Figure out how to derive pub key from the signature
#
def signer(data_to_sign_array):
    to_sign = formatting.binary_string(data_to_sign_array)
    sk = get_signing_key()
    signature = sk.sign_deterministic(to_sign)
    return signature


def verify_sig(sig, signed_data_array):
    to_verify = formatting.binary_string(signed_data_array)
    sk = get_signing_key()
    vk = sk.get_verifying_key()
    try:
        vk.verify(sig, to_verify)
        return True
    except:
        print("invalid sig")
        return False
