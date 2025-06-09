from utils.redis_tool.redis_helper import RedisHelper
from utils.other_tools.aes_encrypt import AESUtils


if __name__ == "__main__":
    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages(
        topic_prefix="dev:op:shadowProp:d-f5701968-w3o1q6nf"
    )
    res = res["dev:op:shadowProp:d-f5701968-w3o1q6nf"]
    print(res)
    aes_encrypt = AESUtils()
    aes_encrypt.encrypt(res['battery_quantity'],)
