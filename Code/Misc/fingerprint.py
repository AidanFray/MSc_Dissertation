import base64
from Crypto.Hash import SHA1
import sys
import re

if len(sys.argv) != 2:
    print("[!] Usage: python signature.py <KEY_FILE>")
    exit()

path = sys.argv[1]

key = None
with open(path, "r") as file:
    key = file.read()

public_key_parts = key.split("\n")
middle = "".join(public_key_parts[2:-3])
middleBytes = base64.b64decode(middle)
middleHex = middleBytes.hex()

# Format from RFC 4880
public_key_len = int(middleHex[2:6], 16)

# Grabs the header and all of the key information
pgp_key_information = middleHex[0:(public_key_len * 2) + 6]

pgp_key_information_bytes = bytes.fromhex(pgp_key_information)

sha1 = SHA1.new()
sha1.update(pgp_key_information_bytes)

fingerprint = sha1.hexdigest().upper()

fingerprint_formatted = " ".join(re.findall(r"....", fingerprint))

print("KEY FINGERPRINT:\n\n\t", fingerprint_formatted)
print()