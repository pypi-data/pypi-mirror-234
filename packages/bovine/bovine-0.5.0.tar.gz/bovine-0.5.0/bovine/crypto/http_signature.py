import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from multiformats import multibase, multicodec

from .helper import did_key_to_public_key, sign_message, verify_signature

logger = logging.getLogger(__name__)


def build_signature(host, method, target):
    return (
        HttpSignature()
        .with_field("(request-target)", f"{method} {target}")
        .with_field("host", host)
    )


class HttpSignature:
    """Helper class to build http signatures

    Usage: Add fields used for signature with `with_fields`. Then
    use `build_signature` or `verify` depending on use case.
    """

    def __init__(self):
        self.fields = []

    def build_signature(self, key_id: str, private_key: str):
        """Returns the signature string when signed with private_key"""
        message = self.build_message()

        signature_string = sign_message(private_key, message)
        headers = " ".join(name for name, _ in self.fields)

        signature_parts = [
            f'keyId="{key_id}"',
            'algorithm="rsa-sha256"',  # FIXME: Should other algorithms be supported?
            f'headers="{headers}"',
            f'signature="{signature_string}"',
        ]

        return ",".join(signature_parts)

    def ed25519_sign(self, private_encoded):
        private_bytes = multicodec.unwrap(multibase.decode(private_encoded))[1]
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)

        message = self.build_message()

        return multibase.encode(private_key.sign(message.encode("utf-8")), "base58btc")

    def ed25519_verify(self, did_key, signature):
        public_key = did_key_to_public_key(did_key)

        signature = multibase.decode(signature)

        message = self.build_message().encode("utf-8")

        try:
            public_key.verify(signature, message)
        except InvalidSignature:
            return False

        return True

    def verify(self, public_key: str, signature: str):
        """Verifies signature"""
        message = self.build_message()
        return verify_signature(public_key, message, signature)

    def build_message(self):
        """Builds the message"""
        return "\n".join(f"{name}: {value}" for name, value in self.fields)

    def with_field(self, field_name, field_value):
        """Adds a field to be used when building a http signature"""
        self.fields.append((field_name, field_value))
        return self

    @property
    def headers(self):
        """Headers as specified when building http signature"""
        return {name: value for name, value in self.fields if name[0] != "("}
