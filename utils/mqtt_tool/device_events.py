import time, base64, uuid, asyncio
from google.protobuf.json_format import ParseDict
from protobuf.protobuf_py import (
    generalBuffData_pb2,
    firmwareVersion_pb2,
    upgradeFirmware_pb2,
    shadowProSet_pb2,
    birdOssEvent_pb2,
    unbindUser_pb2,
    devEventUp_pb2,
)


# 基类
class BaseEvent:
    def __init__(self, device_id: str):
        self.device_id = device_id

    def generate(self) -> bytes:
        raise NotImplementedError("子类必须实现 generate() 方法")

    def random_event_id(self):
        random_str = uuid.uuid4().hex  # 生成32字符十六进制
        part1, part2 = random_str[:6], random_str[6:17]  # 拆分前6位和后续11位
        return f"d-{part1}-{part2}"


# 具体事件类
class FirmwareUpEvent(BaseEvent):
    # 上传固件版本信息
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = firmwareVersion_pb2.VersionResponse()
        data_obj = firmwareVersion_pb2.FirmwareVersionVo

        data = {
            "fmvVer": "1.0.0",
            "socVer": "1.0.0",
            "mcuVer": "1.0.0",
            "wirelessVer": "1.0.0",
            "standby": "1.0.0",
        }

        buff_data = {
            "result": True,
            "objDevId": self.device_id,
            "msg": "success",
            "data": data,
        }

        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "FirmwareUp",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class ShadowGetEvent(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = shadowProSet_pb2.ShadowGetVo()

        buff_data = {
            "objDevId": self.device_id,
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "ShadowGet",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class BirdEvent(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = birdOssEvent_pb2.BirdEventVo()

        buff_data = {
            "objDevId": self.device_id,
            "eventId": self.random_event_id(),
            "ftype": 1,
            "etype": "bird",
            "lableJson": "json",
            "osstype": "30",
            "url": "https://usvideo30.s3.us-west-1.amazonaws.com/20250730/d-8d8b4768-ns6aoiho-1753868888829-thumbnail.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250819T080343Z&X-Amz-SignedHeaders=host&X-Amz-Expires=20000&X-Amz-Credential=AKIAZOWLBZWLWXCNJM75%2F20250819%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=27225aa87c70a0baf044feb46dc91613d54977be618e84d172e93cb3d6dc2b7d",
            "iLen": 0,
            "zeroTm": int(time.time() * 1000),
            "duration": 0,
            "isEncrypt": False,
            "encryptKey": "",
            "localfile": "",
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "BirdEvent",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class DevUnbindEvent(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = unbindUser_pb2.unbindRequest()

        buff_data = {
            "objDevId": self.device_id,
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "DevUnbind",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class EventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.EventVo()

        buff_data = {
            "objDevId": self.device_id,
            "eventId": self.random_event_id(),
            "etype": "person",  # 事件类型: move ：移动 ；penson ：人检测；car: 车检测 : pet : 宠物
            "picUrl": "https://usvideo30.s3.us-west-1.amazonaws.com/20250818/d-8d8b4768-ns6aoiho-1755501431260-thumbnail.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250819T064022Z&X-Amz-SignedHeaders=host&X-Amz-Expires=20000&X-Amz-Credential=AKIAZOWLBZWLWXCNJM75%2F20250819%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=b777b6a14efff1db78a4c54b044d494acf31d46ca0892fa7579e25468cdf5e87",
            "localfile": "test.png",
            "zeroTm": int(time.time() * 1000),
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "EventUp",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class OssEventUp(BaseEvent):
    # 云存储事件上报，用来上传云存储视频，在普通事件之后使用
    def generate(self):
        def generate_event_up(eventId):
            proto_obj = generalBuffData_pb2.GeneralBuffData()
            buff_obj = devEventUp_pb2.EventVo()

            buff_data = {
                "objDevId": self.device_id,
                "eventId": eventId,
                "etype": "person",  # 事件类型: move ：移动 ；penson ：人检测；car: 车检测 : pet : 宠物
                "picUrl": "https://usvideo30.s3.us-west-1.amazonaws.com/20250818/d-8d8b4768-ns6aoiho-1755501431260-thumbnail.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250819T064022Z&X-Amz-SignedHeaders=host&X-Amz-Expires=20000&X-Amz-Credential=AKIAZOWLBZWLWXCNJM75%2F20250819%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=b777b6a14efff1db78a4c54b044d494acf31d46ca0892fa7579e25468cdf5e87",
                "localfile": "test.png",
                "zeroTm": int(time.time() * 1000),
            }
            buff = base64.b64encode(
                ParseDict(buff_data, buff_obj).SerializeToString()
            ).decode()

            protobuf_data = {
                "type": "EventUp",
                "buff": buff,
                "time": int(time.time() * 1000),
                "requestId": "requestId=",
            }
            return ParseDict(protobuf_data, proto_obj).SerializeToString()

        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.OssEventVo()
        eventId = self.random_event_id()
        buff_data = {
            "objDevId": self.device_id,
            "eventId": eventId,
            "osstype": "7",
            "ossUrl": "https://usvideo30.s3.us-west-1.amazonaws.com/20250818/d-8d8b4768-ns6aoiho-1755501431260-thumbnail.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250819T064022Z&X-Amz-SignedHeaders=host&X-Amz-Expires=20000&X-Amz-Credential=AKIAZOWLBZWLWXCNJM75%2F20250819%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=b777b6a14efff1db78a4c54b044d494acf31d46ca0892fa7579e25468cdf5e87",
            "zeroTm": int(time.time() * 1000),
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "OssEventUp",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return [
            generate_event_up(eventId),
            ParseDict(protobuf_data, proto_obj).SerializeToString(),
        ]


class AlarmEventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.AlarmEventVo()
        """
            other = 0; // 其他
            eq = 1; //等于标准值
            gt = 2; //大于
            lt = 3; //小于
            gte = 4; //大于等于
            lte = 5; //小于等于
            in = 6; //in条件
        """
        data = {
            "value": "1",  # 告警值
            "condition": 3,
            "thresholdValue": "30",
            "msg": "test",
        }

        buff_data = {
            "objDevId": self.device_id,
            "eventId": self.random_event_id(),
            "alarmType": "lowBattery",  # 告警事件类型：lowBattery :低电量告警
            "data": data,
            "zeroTm": int(time.time() * 1000),
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "AlarmEventUp",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class UpgradeStateEventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = upgradeFirmware_pb2.UpgradeStateVo()

        buff_data = {
            "objDevId": self.device_id,
            "otaId": "",
            "statusType": 1,  # 0: 未知 1: 下载固件 2: 固件升级状态
            "status": 1,  # 0:未知 1: 成功 2：超时 3：失败
            "msg": "test failed",
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "UpgradeState",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class DevLinkEventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.DevLinkEventVo()

        buff_data = {
            "objDevId": self.device_id,
            "time": int(time.time() * 1000),
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "DevLink",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class CheckCloudPackageEventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.CheckCloudPackageEventVo()

        buff_data = {
            "objDevId": self.device_id,
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "CheckCloudPackage",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


class TelCardEventUp(BaseEvent):
    def generate(self):
        proto_obj = generalBuffData_pb2.GeneralBuffData()
        buff_obj = devEventUp_pb2.TelCardEventVo()

        buff_data = {
            "objDevId": self.device_id,
            "type": 1,  # 0未知 1：正常通知 2：告警通知
            "iccid": 1234567890123456,
            "imsi": "",
            "imei": "",
        }
        buff = base64.b64encode(
            ParseDict(buff_data, buff_obj).SerializeToString()
        ).decode()

        protobuf_data = {
            "type": "TelCard",
            "buff": buff,
            "time": int(time.time() * 1000),
            "requestId": "requestId=",
        }
        return ParseDict(protobuf_data, proto_obj).SerializeToString()


# 工厂
class EventFactory:
    event_map = {
        "FirmwareUp": FirmwareUpEvent,
        "ShadowGet": ShadowGetEvent,
        "BirdEvent": BirdEvent,
        "DevUnbind": DevUnbindEvent,
        "EventUp": EventUp,
        "OssEventUp": OssEventUp,
        "AlarmEventUp": AlarmEventUp,
        "UpgradeState": UpgradeStateEventUp,
        "DevLink": DevLinkEventUp,
        "CheckCloudPackage": CheckCloudPackageEventUp,
        "TelCard": TelCardEventUp,
    }

    @classmethod
    def create_event(cls, event_type: str, device_id: str) -> BaseEvent:
        event_cls = cls.event_map.get(event_type)
        if not event_cls:
            raise ValueError(f"Unsupported event type: {event_type}")
        return event_cls(device_id)


# 主循环
class DeviceLoop:
    def __init__(self, device_id, mqtt_client, logger):
        self.device_id = device_id
        self.mqtt = mqtt_client
        self.logger = logger

    async def device_to_plat_loop(self):
        topic = f"device/general_dev_to_plat/devices/{self.device_id}/send/requestId="

        buff_type_list = ["FirmwareUp", "ShadowGet", "BirdEvent"]

        while True:
            for event_type in buff_type_list:
                event_obj = EventFactory.create_event(event_type, self.device_id)
                protobuf_data = event_obj.generate()

                await self.mqtt.publish(topic, protobuf_data)
                self.logger.info(f"[{self.device_id}] Sent {event_type} event")

            await asyncio.sleep(300)
