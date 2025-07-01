import redis
import json
import time


class RedisHelper:
    def __init__(self, host="47.107.113.31", port=16379, db=3, password="SZlzy0701"):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,  # 自动将 bytes 解码为 str
        )

    def get_cached_messages(self, key):
        """
        获取所有缓存的 MQTT 消息
        :param key: Redis 中存储消息的 key 前缀
        :return: dict {key: payload}
        """
        key_type = self.client.type(key)
        if key_type == "string":
            # 缓存中只有一条消息
            return {key: self.client.get(key)}
        elif key_type == "hash":
            # 缓存中有多条消息
            return self.client.hgetall(key)
        else:
            return {}


if __name__ == "__main__":
    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages("dev:op:shadowProp:d-8d8b4768-ns6aoiho")
    print(res)
    from protobuf.protobuf_py import cmdPro_pb2

    msg = cmdPro_pb2.cmdProRequest()
    for k, v in res.items():
        print(k, msg.ParseFromString(v))
