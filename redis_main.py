import sys
from utils.redis_tool.redis_helper import RedisHelper
import base64

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
from protobuf.protobuf_py import cmdPro_pb2, deviceProp_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson

if __name__ == "__main__":
    import json

    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages("dev:op:shadowProp:d-8d8b4768-ns6aoiho")
    print(res)
    msg = deviceProp_pb2.PropDataVo()
    data = {}
    for k, v in res.items():
        msg.ParseFromString(base64.b64decode(v))
        data[json.loads(k)] = MessageToDict(msg)
    print("================================================")
    print(data)

    from google.protobuf.json_format import ParseDict   

    battery = {'type': 'INTEGER', 'value': '4', 'time': '1756699138775'}
    msg = deviceProp_pb2.PropDataVo()
    ParseDict(battery, msg)
    s_data = base64.b64encode(msg.SerializeToString())
    print(s_data)