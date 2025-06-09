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

    def cache_message(self, topic, payload, expire=3600):
        """
        缓存一条 MQTT 消息
        :param topic: MQTT 主题
        :param payload: 消息内容（可以是 dict）
        :param expire: 过期时间（秒）
        """
        key = f"mqtt:{topic}:{int(time.time())}"
        value = json.dumps(payload)
        self.client.setex(key, expire, value)

    def get_cached_messages(self, topic_prefix="mqtt:"):
        """
        获取所有缓存的 MQTT 消息
        :param topic_prefix: Redis 中存储消息的 key 前缀
        :return: dict {key: payload}
        """
        # checkdev:status:tcp:d-f5701968-jmgm9cqp
        # checkdev:status:mqtt:d-f5701968-jmgm9cqp
        # checkdev:status:p2p:d-f5701968-jmgm9cqp
        keys = self.client.keys(f"{topic_prefix}*")
        print(keys)
        result = {}
        for key in keys:
            key_str = key if isinstance(key, str) else key.decode()
            key_type = self.client.type(key_str)
            if isinstance(key_type, bytes):
                key_type = key_type.decode()
            if key_type == "string":
                result[key_str] = self.client.get(key_str)
            elif key_type == "hash":
                result[key_str] = self.client.hgetall(key_str)
            elif key_type == "list":
                result[key_str] = self.client.lrange(key_str, 0, -1)
            elif key_type == "set":
                result[key_str] = list(self.client.smembers(key_str))
            else:
                result[key_str] = f"<Unsupported type: {key_type}>"

        return result

    def delete_topic_cache(self, topic):
        """
        删除某个 topic 的所有缓存
        """
        keys = self.client.keys(f"mqtt:{topic}:*")
        if keys:
            self.client.delete(*keys)

    def clear_all_cache(self):
        """
        清除所有缓存（仅推荐开发测试环境使用）
        """
        keys = self.client.keys("mqtt:*")
        if keys:
            self.client.delete(*keys)


if __name__ == "__main__":
    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages(
        topic_prefix="dev:op:shadowProp:d-f5701968-jmgm9cqp"
    )
    # res = redis_helper.get_cached_messages(
    #     topic_prefix="checkdev:status:tcp:d-f5701968-jmgm9cqp"
    # )
    print(res)
