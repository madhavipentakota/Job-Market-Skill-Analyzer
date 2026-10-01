"""
Minimal password hashing helpers for the optional auth feature.

Uses Python's built-in hashlib (PBKDF2-HMAC-SHA256) instead of passlib/bcrypt
to avoid a known passlib<->bcrypt version-compatibility issue on fresh
installs. Kept simple and dependency-free; swap for a dedicated auth
library before using this in any real production setting.
"""
import hashlib
import os
import hmac

_ITERATIONS = 200_000


def hash_password(plain_password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, _ITERATIONS)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt_hex, digest_hex = hashed_password.split("$")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    actual = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, _ITERATIONS)
    return hmac.compare_digest(actual, expected)
