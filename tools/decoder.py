"""
Модуль расшифровки объектов площадки Фабрикант
"""

import re
import base64
import hashlib
from phpserialize import loads, dumps
from Cryptodome.Cipher import AES


def decrypt(message, return_digits=False):
    secret_key = 'fabr_key'
    secret_iv = 'fabr_iv'

    base64_message = message + '=='
    base64_bytes = base64_message.encode("ascii")
    decode = base64.b64decode(base64_bytes)

    hash_obj_key = hashlib.sha256(secret_key.encode("ascii"))
    key = hash_obj_key.hexdigest()[:32].encode("utf-8")

    hash_obj_iv = hashlib.sha256(secret_iv.encode("ascii"))
    iv = hash_obj_iv.hexdigest()[:16].encode("utf-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decoded_text = loads(dumps(cipher.decrypt(decode)), decode_strings=True)

    if return_digits:
        return re.search('[0-9]*', decoded_text).group(0)

    return decoded_text.replace('\n', '')
