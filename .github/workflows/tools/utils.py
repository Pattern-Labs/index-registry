import requests
import hashlib
import base64


def download(url: str) -> bytes:
    with requests.get(url) as response:
        return response.content


def integrity(data: bytes) -> str:
    hash_value = hashlib.sha256(data)
    return "sha256-" + base64.b64encode(hash_value.digest()).decode()
