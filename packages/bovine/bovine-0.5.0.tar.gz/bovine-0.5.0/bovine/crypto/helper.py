import base64
import hashlib
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from multiformats import multibase, multicodec

logger = logging.getLogger(__name__)


def content_digest_sha256(content: str | bytes) -> str:
    """Computes the SHA256 digest of given content"""
    if isinstance(content, str):
        content = content.encode("utf-8")

    digest = base64.standard_b64encode(hashlib.sha256(content).digest()).decode("utf-8")
    return "sha-256=" + digest


def sign_message(private_key, message):
    try:
        key = load_pem_private_key(private_key.encode("utf-8"), password=None)
        assert isinstance(key, rsa.RSAPrivateKey)
    except Exception as e:
        logger.error(e)
        logger.error(private_key)
        raise (e)

    return base64.standard_b64encode(
        key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    ).decode("utf-8")


def verify_signature(public_key, message, signature):
    public_key_loaded = load_pem_public_key(public_key.encode("utf-8"))

    assert isinstance(public_key_loaded, rsa.RSAPublicKey)

    try:
        public_key_loaded.verify(
            base64.standard_b64decode(signature),
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        logger.warning("invalid signature")
        return False

    return True


def public_key_to_did_key(public_key: ed25519.Ed25519PublicKey) -> str:
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    wrapped = multicodec.wrap("ed25519-pub", public_bytes)
    encoded = multibase.encode(wrapped, "base58btc")

    return "did:key:" + encoded


def did_key_to_public_key(did: str) -> ed25519.Ed25519PublicKey:
    assert did.startswith("did:key:")
    decoded = multibase.decode(did[8:])
    codec, key_bytes = multicodec.unwrap(decoded)
    assert codec.name == "ed25519-pub"

    return ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)


def private_key_to_ed25519(private_key_str: str) -> ed25519.Ed25519PrivateKey:
    decoded = multibase.decode(private_key_str)
    codec, key_bytes = multicodec.unwrap(decoded)
    assert codec.name == "ed25519-priv"

    return ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes)
