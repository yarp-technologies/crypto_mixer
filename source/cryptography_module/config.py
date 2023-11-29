import os
from rsa import PublicKey, PrivateKey

BYTES_TO_STR_FORMAT = "utf-8"

PUBLIC_KEY_PEM = os.environ.get('RSA_PUBLIC_KEY_PEM')
PRIVATE_KEY_PEM = os.environ.get('RSA_PRIVATE_KEY_PEM')

PUBLIC_KEY = PublicKey.load_pkcs1(PUBLIC_KEY_PEM, format="PEM")
PRIVATE_KEY = PrivateKey.load_pkcs1(PRIVATE_KEY_PEM, format="PEM")
