
from __future__ import annotations
from secrets import token_hex
from hashlib import md5

def generate_random_key() -> str:
    return token_hex(8)

def login_hash(password: str, rndk: str) -> str | bytes:
    key = encrypt_password(password, False)
    key += rndk
    key += 'Y(02.>\'H}t":E1'
    return encrypt_password(key)

def encrypt_password(password: str, digest: bool = True) -> str:
    if digest:
        password = generate_hash(password)

    swapped_hash = password[16:32] + password[0:16]
    return swapped_hash

def generate_hash(undigested: str | int | bytes) -> str:
    if type(undigested) == str:
        undigested = undigested.encode('utf-8')
    elif type(undigested) == int:
        undigested = str(undigested).encode('utf-8')
    return md5(undigested).hexdigest()
