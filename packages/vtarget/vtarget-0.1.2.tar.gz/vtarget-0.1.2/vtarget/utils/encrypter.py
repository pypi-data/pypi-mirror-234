import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# https://medium.com/@sachadehe/encrypt-decrypt-data-between-python-3-and-javascript-true-aes-algorithm-7c4e2fa3a9ff


class Encrypter:
    def encrypt(self, data: str, key: str, iv: str = "VTVTVTVTVTVTVTVT"):
        iv = iv.encode("utf-8")  # 16 char for AES128
        data = pad(data.encode(), 16)
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(data))

    def decrypt(self, enc: str, key: str, iv: str = "VTVTVTVTVTVTVTVT"):
        iv = iv.encode("utf-8")  # 16 char for AES128
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
        b = unpad(cipher.decrypt(enc), 16)
        return b.decode("utf-8")


encrypter = Encrypter()
