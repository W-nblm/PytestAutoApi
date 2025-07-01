import sys
from utils.redis_tool.redis_helper import RedisHelper

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
from protobuf.protobuf_py import cmdPro_pb2


if __name__ == "__main__":

    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages("dev:op:shadowProp:d-8d8b4768-ns6aoiho")
    print(res)
    msg = cmdPro_pb2.CmdProRequest()

    for k, v in res.items():
        msg.ParseFromString(v)
        print(msg)
