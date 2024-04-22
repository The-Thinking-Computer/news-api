import json
import hashlib
import uuid
import os
import random
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

def generate_random_message(length=32):
    """Generate a random message of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')

def key_checker(private_key_path, public_key_path):
    """
    Check if the provided public key corresponds to the private key.

    Args:
        private_key_path (str): Path to the private key file.
        public_key_path (str): Path to the public key file.

    Returns:
        bool: True if the public key corresponds to the private key, False otherwise.
    """
    try:
        with open(private_key_path, "rb") as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None
            )

        with open(public_key_path, "rb") as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read()
            )

        message = generate_random_message()
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception as e:
        print(f"Key pair verification failed: {e}")
        return False

def validate_input(data):
    """
    Validate the input data to ensure it adheres to the specified JSON structure.

    Args:
        data (bytes): The input data to be validated.

    Returns:
        bool: True if the input data is valid, False otherwise.
    """
    try:
        json_str = data.decode('utf-8')
        json_data = json.loads(json_str)
        if isinstance(json_data, dict) and \
           'id' in json_data and isinstance(json_data['id'], str) and uuid.UUID(json_data['id']) and \
           'parent_url' in json_data and isinstance(json_data['parent_url'], str) and \
           'link' in json_data and isinstance(json_data['link'], str) and \
           'content' in json_data and isinstance(json_data['content'], dict) and \
           'title' in json_data['content'] and isinstance(json_data['content']['title'], str) and \
           'author' in json_data['content'] and isinstance(json_data['content']['author'], str) and \
           'description' in json_data['content'] and isinstance(json_data['content']['description'], str) and \
           'article_content' in json_data['content'] and json_data['content']['article_content'] == 'NOT AVAILABLE':
            return True
    except Exception as e:
        print(f"Error during input validation: {str(e)}")

    return False

class DigitalSignatureGenerator:
     """
    A class for generating digital signatures using a private key.

    This class provides functionality to generate digital signatures using a private key. 
    The digital signatures can be used for data authentication and integrity verification.

    Attributes:
    - private_key_path (object): The private key used for generating digital signatures.

    Methods:
    - __init__: Initializes the DigitalSignatureGenerator object with a private key.
    """
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
