from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from exceptions.exception import (
    KeyGeneratorGenerateRSAKeypairException,
    KeyGeneratorCreatePublicKeyPemException,
)


class KeyGenerator:
    @staticmethod
    async def generate_rsa_keypair(public_exponent=65537, key_size=2048):
        try:
            private_key = rsa.generate_private_key(
                public_exponent=public_exponent,
                key_size=key_size,
                backend=default_backend(),
            )
            public_key = private_key.public_key()
        except Exception:
            raise KeyGeneratorGenerateRSAKeypairException

        return private_key, public_key

    @staticmethod
    async def create_public_key_pem(public_key):
        try:
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,

            )
        except Exception:
            raise KeyGeneratorCreatePublicKeyPemException

        return public_key_pem
