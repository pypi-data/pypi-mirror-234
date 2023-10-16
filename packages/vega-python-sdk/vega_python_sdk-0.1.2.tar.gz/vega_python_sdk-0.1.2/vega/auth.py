from logging import getLogger
from bip_utils import (
    Bip32Slip10Ed25519,
    Bip39SeedGenerator,
)
from hashlib import sha3_256


logger = getLogger(__name__)

FIRST_HARDENED_IDX = 2147483648
MAGIC_NB = 1789
ORIGIN_IDX = FIRST_HARDENED_IDX + MAGIC_NB


class Signer:
    def __init__(self, ed25519_signer: Bip32Slip10Ed25519):
        self._signer = ed25519_signer
        self._pub_key = self._signer.PublicKey().RawCompressed().ToHex()[2:]

    @classmethod
    def from_mnemonic(cls: "Signer", mnemonic: str, derivations: int = 1) -> "Signer":
        return Signer(
            ed25519_signer=Bip32Slip10Ed25519.FromSeed(
                Bip39SeedGenerator(mnemonic).Generate()
            ).DerivePath(
                f"m/{ORIGIN_IDX}'/{FIRST_HARDENED_IDX}'/{FIRST_HARDENED_IDX + derivations}'"
            )
        )

    @classmethod
    def from_private_key(cls: "Signer", private_key: str) -> "Signer":
        return Signer(
            ed25519_signer=Bip32Slip10Ed25519.FromPrivateKey(bytes.fromhex(private_key))
        )

    def sign(self, to_sign: bytes):
        return (
            self._signer.PrivateKey()
            .KeyObject()
            .UnderlyingObject()
            .sign(sha3_256(to_sign).digest())[:64]
        )
