from dataclasses import dataclass
import logging

from typing import List

logger = logging.getLogger(__name__)


@dataclass
class Signature:
    """Helper class to parse HTTP Signatures"""

    key_id: str
    algorithm: str
    headers: dict
    signature: str

    def __post_init__(self):
        if self.algorithm not in ["rsa-sha256", "hs2019"]:
            logger.error(f"Unsupported algorithm {self.algorithm}")
            logger.error(self.signature)
            logger.error(self.headers)
            logger.error(self.key_id)

            raise ValueError("Unsupported algorithm", self.algorithm)

    @property
    def fields(self) -> List[str]:
        """Returns the fields that are used when building the signature"""
        return self.headers.split(" ")

    @staticmethod
    def from_signature_header(header):
        """Takes the signature header and turns into Signature object

        The header is assumed of the for key=value,... The keys keyId,
        algorithm, headers, and signature are parsed. If algorithm
        is absent it is assumed to be rsa-sha256. The other keys are required.
        """
        headers = header.split(",")
        headers = [x.split('="', 1) for x in headers]
        parsed = {x[0]: x[1].replace('"', "") for x in headers}

        return Signature(
            parsed["keyId"],
            parsed.get("algorithm", "rsa-sha256"),
            parsed["headers"],
            parsed["signature"],
        )


def parse_signature_header(header):
    return Signature.from_signature_header(header)
