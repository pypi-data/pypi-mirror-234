from __future__ import annotations

import binascii
from nacl.bindings import (crypto_pwhash_alg,
                           randombytes as secure_random_bytes,
                           crypto_sign_seed_keypair,
                           crypto_sign_open,
                           crypto_sign,
                           sodium_memcmp,
                           sodium_add,
                           crypto_pwhash_SALTBYTES as SALT_BYTES,
                           crypto_secretbox_NONCEBYTES as NONCE_BYTES,
                           crypto_pwhash_BYTES_MIN as KEY_BYTES,
                           crypto_sign_BYTES as SIGN_BYTES)
from nacl.exceptions import BadSignatureError
from nacl.pwhash.argon2id import (OPSLIMIT_MIN as OPS_LIMIT,
                                  MEMLIMIT_MIN as MEM_LIMIT,
                                  ALG)
import nacl.utils
from typing import Optional, Tuple


def __nonce_plus():
    """
    Generates a bytes structure representing a 1
    """
    # I have no doubt there will be a better way of doing this.
    zeros = b"\0" * (NONCE_BYTES - 1)
    one = b"\1"
    return zeros + one


__one = __nonce_plus()  # store it as a constant


def salt_bytes() -> int:
    """
    Returns the length of salt in bytes
    """
    return SALT_BYTES


def nonce_bytes() -> int:
    """
    Returns the length of a nonce in bytes
    """
    return NONCE_BYTES


def signature_bytes() -> int:
    """
    Returns the length of a signature
    """
    return SIGN_BYTES


def verify_key_bytes() -> int:
    """
    Returns the length of a public signature key
    """
    return 32


def generate_random_password() -> bytes:
    return binascii.hexlify(nacl.utils.random())


def generate_salt() -> bytes:
    """
    Creates a randomly secure salt.

    This method is usually executed by the client to create 
    a new sign certificate derived from this salt and his 
    own password.

    The salt and the public part of the signing pair can 
    be freely transmitted, even through insecure channels.

    """
    return secure_random_bytes(SALT_BYTES)


def generate_nonce(previous: Optional[bytes] = None) -> bytes:
    """
    Generates a new nonce

    This method is usually executed by the server to create a 
    challenge that has to be signed by the client.

    Parameters
    ----------
    previous: bytes, optional, defaults to None
        Previous nonce used.  When set, the new nonce will be the 
        previous nonce plus one.  The addition is done following 
        the addition arithmetic found in libsodium.  When previous 
        is left unset (None), the function creates a new,
        randomly secure, nonce

    """
    if previous is None:
        return secure_random_bytes(NONCE_BYTES)

    if len(previous) != NONCE_BYTES:
        raise ValueError(f"Base nonce has to be of {NONCE_BYTES} length")

    global __one
    return sodium_add(previous, __one)


def derive_signature_keys(salt: bytes, password: bytes) -> Tuple[bytes, bytes]:
    """
    Based on a salt and a user provided password, a new password is derived 
    using argon2i.  This password is used to derive a signature pair.
    """
    # derive a cryptographically sound password out of
    # the user password and a salt.
    seed = crypto_pwhash_alg(KEY_BYTES * 2, password, salt, OPS_LIMIT, MEM_LIMIT, ALG)
    return crypto_sign_seed_keypair(seed)


def derive_verify_key(salt: bytes, password: bytes) -> bytes:
    """
    Computes and returns the public verification key
    """
    # use the derived password as seed to create a signing key par
    verify_key, _ = derive_signature_keys(salt, password)
    # return the public part of the key, which is safe to be transmitted, sent,
    # stored by any 3rd party that wants to validate signatures.
    return verify_key


def sign(message: bytes, sk: bytes) -> bytes:
    raw_signed = crypto_sign(message, sk)
    return raw_signed[:SIGN_BYTES]


def verify(message: bytes, signature: bytes, pk: bytes) -> bool:
    try:
        return sodium_memcmp(message, crypto_sign_open(signature + message, pk))
    except BadSignatureError:
        return False


def sign_challenge(salt: bytes, nonce: bytes, password: bytes) -> bytes:
    """
    Signs a nonce with the signature key generated from computing a new 
    password derived from the salt and user provided password.
    """
    # use the derived password as seed to create a signing key par
    _, signing_key = derive_signature_keys(salt, password)
    # use the private part (signing_key) to sign the nonce
    raw_signed = crypto_sign(nonce, signing_key)
    # extract the signature bytes (as the result combines both the nonce and the signature)
    return raw_signed[:SIGN_BYTES]


def compare_buffers(a: bytes, b: bytes) -> bool:
    """
    Test that compares two regions of memory in constant time.
    """
    return sodium_memcmp(a, b)


def verify_challenge(token: bytes, nonce: bytes, verify_key: bytes) -> bool:
    """
    Checks the signature of `nonce` can be verified with the public 
    verification key.

    Parameter
    ---------
    token: bytes
        Signature obtained at the client side

    nonce: bytes
        Payload that generate the signature

    verify_key: bytes 
        Public key associated with the client.
    """

    # recombine the buffers in the expected libsodium format
    message = token + nonce
    try:
        # check the signature using the verify key
        # this method either blows or returns the
        # original message
        open = crypto_sign_open(message, verify_key)
        # a little bit unnecessary, but the next
        # step compares the output of the open
        # function with the original nonce.
        return sodium_memcmp(nonce, open)
    except BadSignatureError:
        return False


__all__ = [
    'verify_challenge', 'sign_challenge', 'derive_verify_key',
    'signature_bytes', 'nonce_bytes', 'salt_bytes', 'compare_buffers', 'generate_random_password'
]

if __name__ == "__main__":
    import base64

    salt = generate_salt()
    password = generate_random_password()
    pk, sk = derive_signature_keys(salt, password)
    print("pk: ", base64.b64encode(pk).decode('ascii'))
    print("sk: ", base64.b64encode(sk).decode('ascii'))
