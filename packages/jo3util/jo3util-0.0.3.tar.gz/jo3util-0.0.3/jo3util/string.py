#! /usr/bin/env python3
# vim:fenc=utf-8
from hashlib import sha256

def hash_string(string: str) -> str:
    return sha256(string.encode('utf-8'),
                  usedforsecurity=False).hexdigest()

