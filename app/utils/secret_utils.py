import base64
import hashlib
from json import dumps

from Crypto import Random
from Crypto.Cipher import AES

from app.database.models.secret import Secret

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
    BLOCK_SIZE - len(s) % BLOCK_SIZE
)
unpad = lambda s: s[: -ord(s[len(s) - 1 :])]


def encrypt_secret(secret: Secret) -> bytes:
    private_key = hashlib.sha256(secret.code_phrase.encode("utf-8")).digest()
    raw = pad(secret.secret_body)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8")))


def decrypt_secret(secret: Secret, code_phrase: str) -> str:
    private_key = hashlib.sha256(code_phrase.encode("utf-8")).digest()
    enc = base64.b64decode(secret.secret_body)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(cipher.decrypt(enc[16:])))
