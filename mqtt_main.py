from utils.mqtt_tool.devices import DeviceModel
from utils.mqtt_tool.mqtt import Mqtt
import sys
from utils.redis_tool.redis_helper import RedisHelper
import enum

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
from enum import Enum


class CommandType(Enum):
    temperature_mark_sw = "温度开关"
    time_watermark = "时间水印"
    pir_sensitivity = "人体感应灵敏度"
    infrared_sw = "红外开关"
    sd_status = "SD卡状态"
    sd_capacity = "SD卡容量"
    sd_formatting = "SD卡格式化"
    feed_plan_sw = "喂食计划开关"
    detect_person_switch = "检测到人开关"
    volume_set = "音量设置"
    battery_quantity = "电池电量"
    anti_flicker = "防眩晕"
    detect_time = "检测时间"
    rt_v_bird_quality = "实时视频鸟类质量"
    hand_feed = "手动喂食"
    basic_osd = "基础OSD"
    basic_indicator = "基础指示灯"


if __name__ == "__main__":
    # mqtt = Mqtt(device_id="d-f5701968-w3o1q6nf")
    # mqtt.client_loop_forever()
    # mqtt.client_disconnect()
    from protobuf.protobuf_py import deviceProp_pb2
    from protobuf.protobuf_py import modelType_pb2
    import base64

    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages(
        topic_prefix="dev:op:shadowProp:d-s240012"
    )
    res = res["dev:op:shadowProp:d-s240012"]
    # ENUM = 1;
    # INTEGER = 2;
    # FLOAT = 3;
    # STRING = 4;
    # JSON = 5;
    # RAW = 6;

    result = {}
    for key, value in res.items():
        ntpResponse = deviceProp_pb2.PropDataVo()
        ntpResponse.ParseFromString(base64.b64decode(value))

        data = {}
        data["type"] = modelType_pb2.ModelType.Name(ntpResponse.type)
        data["value"] = ntpResponse.value
        data["time"] = ntpResponse.time
        result[key] = data

    print(result)
