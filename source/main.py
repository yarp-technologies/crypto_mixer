from cryptography_module import encode_data, decode_data
from database.models import Wallet

pk = "abc"

wallet = Wallet(address="123", private_key=pk)

print(wallet.private_key)
print(wallet.decoded_private_key)
