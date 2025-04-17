from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64


def rsa_encrypt(cls, timestamp: str):
    """校验RSA加密 使用公钥进行加密"""
    publickey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBEzfkqyRkOB9WDqdmJrkZHPu6BkuXK5rxtciKhegltnJ4BODDFB44RT0wbHB8xzGbQvW3AzKHDvP2Me8kLzWhyJ4nbTpW84gQ6Q0jgJIoY3/OUrWl24/VhoutJs3ivCQAuj7RDYB+pei3TxaZ0dngWfPX7up7MDqE8FNpzXeadQIDAQAB"
    public_key = (
        "-----BEGIN PUBLIC KEY-----\n" + publickey + "\n-----END PUBLIC KEY-----"
    )
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    cipher_text = base64.b64encode(cipher.encrypt(timestamp.encode())).decode()
    return cipher_text