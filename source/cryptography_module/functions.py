from .config import PUBLIC_KEY, PRIVATE_KEY, BYTES_TO_STR_FORMAT
from rsa import encrypt, decrypt


def encode_data(data: str) -> str:
    encrypted = encrypt(data.encode(encoding=BYTES_TO_STR_FORMAT), PUBLIC_KEY)
    return encrypted.hex()

def decode_data(data: str) -> str:
    bytes_data = bytes.fromhex(data)
    decrypted = decrypt(bytes_data, PRIVATE_KEY)
    return decrypted.decode(encoding=BYTES_TO_STR_FORMAT)
