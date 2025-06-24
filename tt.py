# import requests
# import time


# def get_public_ip(retries=50, delay=5):
#     for attempt in range(1, retries + 1):
#         try:
#             ip = requests.get("https://ipinfo.io/ip", timeout=5).text.strip()
#             print(f"[{attempt}] Got public IP: {ip}")
#             return ip
#         except requests.RequestException as e:
#             print(f"[{attempt}] Failed to get public IP: {e}")
#             if attempt < retries:
#                 time.sleep(delay)
#     print("Exceeded maximum retry attempts to fetch public IP.")
#     return None


# def get_record_id(dns_name, zone_id, token):
#     resp = requests.get(
#         "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records",
#         headers={
#             "Authorization": "Bearer " + token,
#             "Content-Type": "application/json",
#         },
#     )
#     print(resp.json())
#     if not resp.json()["success"]:
#         return None

#     domains = resp.json()["result"]
#     for domain in domains:
#         if dns_name == domain["name"]:
#             return domain["id"]
#     return None


# def update_record(dns_name, zone_id, token, dns_id, ip, proxied=False):
#     resp = requests.put(
#         "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(
#             zone_id, dns_id
#         ),
#         json={"type": "A", "name": dns_name, "content": ip, "proxied": proxied},
#         headers={
#             "Authorization": "Bearer " + token,
#             "Content-Type": "application/json",
#         },
#     )
#     if not resp.json()["success"]:
#         return False
#     return True


# if __name__ == "__main__":
#     token = "QURYiz77jmDV8NoMcBqBQCVCFFDNk18LMPsM__Xd"
#     zone_id = "2d2bcfe7a92e97da138f5d83b350b8f6"
#     dns_name = "66532523.xyz"
#     dns_id = get_record_id(dns_name, zone_id, token)

#     ip = get_public_ip()
#     print(ip)
#     # if not ip:
#     #     exit(1)
#     # sdfsd
#     # update_record(dns_name, zone_id, token, dns_id, ip)
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import base64

def try_decrypt(authKey_b64, keys_to_try):
    cipher_data = base64.b64decode(authKey_b64)
    for key in keys_to_try:
        try:
            des = DES.new(key.encode('utf-8'), DES.MODE_ECB)
            decrypted = des.decrypt(cipher_data)
            try:
                decrypted_text = unpad(decrypted, DES.block_size).decode('utf-8')
            except:
                decrypted_text = decrypted.decode('utf-8')
            print(f"[成功] key: {key} => {decrypted_text}")
        except Exception as e:
            print(f"[失败] key: {key} => {e}")

# authKey
authKey = "1+kerOsP0wPDscT3CFVs1y5y5sL9cgz0P1gOIZpCrzyLIvX44ImzaxgCJ6IyroBv"

# 尝试这些 key（自己补充你项目里可能用的）
possible_keys = [
    "00000000",
    "requestI",
    "iotkey01",
    "12345678",
    "abcdefgh",
    "d-8d8b47",  # requestId[:8]
    "p-0c947c",  # productId[:8]
    "8d8b4768",
    "ns6aoiho",
    "0c947c67",
    "8ghjjvw3"
]

try_decrypt(authKey, possible_keys)
