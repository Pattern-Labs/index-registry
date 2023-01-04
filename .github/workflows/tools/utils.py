import hashlib
import base64


def integrity(data: bytes) -> str:
    hash_value = hashlib.sha256(data)
    return "sha256-" + base64.b64encode(hash_value.digest()).decode()
