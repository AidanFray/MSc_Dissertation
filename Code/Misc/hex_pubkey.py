import base64
import sys

"""
Script that converts hex to public key packet for Gpg
"""


string = sys.argv[1]

b = bytes.fromhex(string);

print("-----BEGIN PGP PUBLIC KEY BLOCK-----")
print()
print(base64.b64encode(b).decode("utf-8"))
print("-----END PGP PUBLIC KEY BLOCK-----")