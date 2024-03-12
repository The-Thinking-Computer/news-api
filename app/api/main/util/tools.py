import os
from datetime import datetime
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
def get_most_recent_file(relative_path):
    folder_path = os.path.abspath(relative_path)
    files = os.listdir(folder_path)
    files = [file for file in files if file.startswith("data__") and file.endswith(".json")]

    if not files:
        return None 
    file_timestamps = [datetime.strptime(file.split("__")[1].split(".json")[0], "%Y-%m-%d_%H-%M-%S") for file in files]

    most_recent_timestamp = max(file_timestamps)
    most_recent_index = file_timestamps.index(most_recent_timestamp)
    return os.path.join(folder_path, files[most_recent_index])

def create_master_key():
    pass
def create_private_key(public_exponent,key_size,backend=default_backend()):
    return rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
def sign_data(key,message):
    return private_key.sign(
        message,
        padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
)


