import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESUtils:

    @staticmethod
    def encrypt(data: str, key: str) -> str:
        key_bytes = key.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_data = pad(data.encode("utf-8"), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode("utf-8")

    @staticmethod
    def decrypt(encrypted_data: str, key: str) -> str:
        key_bytes = key.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decoded_data = base64.b64decode(encrypted_data)
        decrypted = unpad(cipher.decrypt(decoded_data), AES.block_size)
        return decrypted.decode("utf-8")


if __name__ == '__main__':
    
    aes = AESUtils()
    data = "p6QuBDGAwUJpSYJmpuXh4pwi7e5IrAu630Qf+mQi4djPsteiOr6QDJgCbWPUptrtl9OR1ePHwXQ8+K2Scq5/8w=="
    key = "qSkAYaSj1SbdJblgx9+1747812443533"
    # data="CAESE2QtOGQ4YjQ3NjgtbnM2YW9paG8="
    # key="103-98805268-t8252pg+1750266133590"
    # encrypted_data = aes.encrypt(data, key)
    # print(encrypted_data)
    decrypted_data = aes.decrypt(data, key)
    print(decrypted_data)