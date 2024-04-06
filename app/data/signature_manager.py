import json
import hashlib
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class DigitalSignatureGenerator:
    def __init__(self, private_key_path):
        with open(private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def generate_signature(self, data):
        """
        Generate a digital signature for the provided JSON data.
        
        Args:
            data (dict): The JSON data to be signed.

        Returns:
            bytes: The generated digital signature.
        """
 
        serialized_data = json.dumps(data, sort_keys=True).encode('utf-8')
        digest = hashlib.sha256(serialized_data).digest()
        signature = self.private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature
    
    def generate_hash(self, signed_data):
        """
        Generate a hash of the signed data.
        
        Args:
            signed_data (dict): The signed data.

        Returns:
            bytes: The hash of the signed data.
        """
        serialized_signed_data = json.dumps(signed_data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized_signed_data).digest()

    def verify_signature(self, signed_data, public_key):
        """
        Verify the signature of the signed data using the provided public key.
        
        Args:
            signed_data (dict): The signed data containing "data" and "hash" keys.
            public_key: The public key used for verification.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        data = signed_data.get("data", None)
        signature = data.get("signature", None)
        hash_value = signed_data.get("hash", None)
        
        if data is None or signature is None or hash_value is None:
            return False
        
        serialized_data = json.dumps(data, sort_keys=True).encode('utf-8')
        digest = hashlib.sha256(serialized_data).digest()
        
        try:
            public_key.verify(
                signature,
                digest,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            computed_hash = hashlib.sha256(serialized_data).digest()
            return computed_hash == hash_value
        except:
            return False
