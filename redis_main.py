import sys
from utils.redis_tool.redis_helper import RedisHelper
import base64

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
from protobuf.protobuf_py import cmdPro_pb2, deviceProp_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson

if __name__ == "__main__":

    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages("dev:op:shadowProp:d-8d8b4768-ns6aoiho")
    print(res)
    msg = deviceProp_pb2.PropDataVo()
    data = {}
    for k, v in res.items():
        msg.ParseFromString(base64.b64decode(v))
        data[k] = MessageToDict(msg)
    print(data)
