from Crypto.Cipher import DES
import base64
import time

def pad(text: bytes) -> bytes:
    """PKCS5/PKCS7 填充"""
    pad_len = 8 - (len(text) % 8)
    return text + bytes([pad_len] * pad_len)

def generate_auth_key(device_id: str, secret_key: str) -> str:
    # 获取当前秒级时间戳
    timestamp = str(int(time.time()*1000))
    
    # 拼接 deviceId + "_" + time
    plain_text = f"{device_id}_{timestamp}"
    
    # # DES 加密需要密钥长度 8 字节
    # if len(secret_key) != 8:
    #     raise ValueError("DES 密钥必须是 8 字节长度")
    
    # 初始化 DES（ECB 模式）
    cipher = DES.new(secret_key.encode('utf-8'), DES.MODE_ECB)
    
    # PKCS5 填充并加密
    encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8')))
    
    # Base64 编码
    auth_key = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return auth_key, timestamp


if __name__ == "__main__":
    request_id = "d-8d8b4768-ns6aoiho"
    secret = "00000000"  # 8 字节的 DES 密钥
    auth_key, ts = generate_auth_key(request_id, secret)
    print("timestamp:", ts)
    print("authKey:", auth_key)
