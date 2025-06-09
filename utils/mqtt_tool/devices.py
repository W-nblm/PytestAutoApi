import base64
import time
from utils.mqtt_tool.mqtt import Mqtt
from google.protobuf.json_format import ParseDict
import uuid
from enum import Enum
from utils.logging_tool.log_control import INFO, ERROR, WARNING


class CommandType(Enum):
    FirmwareUp = "FirmwareUp"  #:设备上传固件版本"
    ShadowGet = "ShadowGet"  #:设备主动获取一需要更新的影子设备属性"
    DevUnbind = "DevUnbind"  #:设备主动请求解绑"
    EventUp = "EventUp"  #:普通事件上报（只上传图片）"
    OssEventUp = "OssEventUp"  #:云事件上报（上报需要开通云存储功能）"
    UpgradeState = "UpgradeState"  #:升级固件状态上报"
    AlarmEventUp = "AlarmEventUp"  #:告警事件上报"
    DevLink = "DevLink"  #:设备休眠后开始连接，代表设备从休眠开始上线"
    CheckCloudPackage = (
        "CheckCloudPackage"  # 设备在套餐快过期时主动请求后台获取是否有新套餐信息
    )
    TelCard = "TelCard"  #:上传4g卡消息"


class DeviceModel:
    """
    #设备ntp时间校对
    请求: device/ntp/devices/${device_id}/send/requestId=
    返回: device/ntp/devices/${device_id}/response/requestId=

    # 命令请求
    请求: {plat|app}/commands/home/{home_id}/devices/${device_id}/send/requestId=
    返回: {plat|app}/commands/home/${home_id}/devices/${device_id}/response/requestId=

    # 获取属性
    请求: {plat|app}/properties_get/home/${home_id}/devices/${device_id}/send/requestId=
    返回: {plat|app}/properties_get/home/${home_id}/devices/${device_id}/response/requestId=

    # 设备属性自动上报
    请求: plat/properties/home/{home_id}/devices/{device_id}/report

    # 设备心跳包
    请求: device/keeplive/devices/${device_id}/up

    # 配网激活
    请求: device/network/devices/{device_id}/send/requestId=
    返回: device/network/devices/{device_id}/response/requestId=
    # 命令共用topic,平台先请求设备
    请求: plat/general_plat_to_dev/devices/${device_id}/send/requestId=
    返回: plat/general_plat_to_dev/devices/${device_id}/response/requestId=

    # 命令共用topic,设备先请求平台
    请求: device/general_dev_to_plat/devices/${device_id}/send/requestId=
    返回: device/general_dev_to_plat/devices/${device_id}/response/requestId=
    """

    def __init__(self, device_id="wyl123111") -> None:
        # 初始化mqtt
        self.client = Mqtt(device_id=device_id)

    def ntp_time(self, device_id="wyl123111"):
        # 设备ntp时间校对
        # 请求: device/ntp/devices/${device_id}/send/requestId=
        # 返回: device/ntp/devices/${device_id}/response/requestId=
        pub_topic = f"device/ntp/devices/{device_id}/send/requestId={timestmp}"
        requestId = int(time.time() * 1000)
        timestmp = requestId

        from protobuf.protobuf_py import ntpTime_pb2

        request_protobuf = ntpTime_pb2.NtpRequest()
        request_protobuf.deviceSendTime = timestmp
        request_protobuf_serialize = request_protobuf.SerializeToString()

        self.client.client_publish(pub_topic, request_protobuf_serialize)

    def event_up(self, device_id="wyl123111", userId=""):
        pu_topic = f"device/general_dev_to_plat/devices/{device_id}/send/requestId="
        from protobuf.protobuf_py import generalBuffData_pb2
        from protobuf.protobuf_py import devEventUp_pb2
        from protobuf.protobuf_py import modelType_pb2

        alarm_data = devEventUp_pb2.AlarmData()
        alarm_data.modelCode
        alarm_data.value = "10"
        alarm_data.codeType = modelType_pb2.ModelType.ENUM
        alarm_data.condition = devEventUp_pb2.AlarmCondition.eq
        alarm_data.thresholdValue = "11"
        alarm_data.msg = "电量不足,wyl"

        buff_protobuf = devEventUp_pb2.AlarmEventVo()
        buff_protobuf.objDevId = device_id
        buff_protobuf.eventId = "wyk"
        buff_protobuf.alarmType = "lowBattery"
        buff_protobuf.data.CopyFrom(alarm_data)
        buff_protobuf.zeroTm = int(time.time() * 1000)
        buff_protobuf.TmZone = "UTC+8"
        buff_protobuf.userId = userId
        buff_protobuf.devName = "wyk"
        buff_protobuf.jsonInfo = '{"name":"wyk"}'

        serialized_data = buff_protobuf.SerializeToString()

        request_protobuf = generalBuffData_pb2.GeneralBuffData()
        request_protobuf.type = CommandType.EventUp.value
        request_protobuf.buff = base64.b64encode(serialized_data)
        request_protobuf.time = int(time.time() * 1000)
        request_protobuf.requestId = "wyktest"

        serialized_re = request_protobuf.SerializeToString()
        self.client.client_publish(pu_topic, serialized_re)

    def get_attribute(self):
        pass

    def attribute_report(self, home_id="wykhome", device_id="wyl123111"):
        # plat/properties/home/{home_id}/devices/{device_id}/report
        pus_topic = f"plat/properties/home/{home_id}/devices/{device_id}/report"
        from protobuf.protobuf_py import cmdPro_pb2

        request_protobuf = cmdPro_pb2.CmdProResponse()
        request_protobuf.result = 1
        request_protobuf.objDevId = device_id
        request_protobuf.msg = "wyk test"
        request_protobuf.productId = "p-379d8164-im60dioh"
        request_protobuf.optype = cmdPro_pb2.opType.Property
        request_protobuf.data.code = "basic_indicator"
        request_protobuf.data.type = cmdPro_pb2.modelType__pb2.ModelType.INTEGER
        request_protobuf.data.value = "6"

        request_protobuf_serialize = request_protobuf.SerializeToString()
        self.client.client_publish(pus_topic, request_protobuf_serialize)

    def device_keeplive(self, device_id="wyl123111"):
        # 请求: device/keeplive/devices/${device_id}/up
        pus_topic = f"device/keeplive/devices/{device_id}/up"
        from protobuf.protobuf_py import keeplive_pb2

        request_protobuf = keeplive_pb2.keeplive()
        request_protobuf.objDevId = device_id
        request_protobuf.status = 1
        request_protobuf.time = int(time.time() * 1000)
        request_protobuf_serialize = request_protobuf.SerializeToString()

        self.client.client_publish(pus_topic, request_protobuf_serialize)

    def device_activation(
        self,
        device_id="wyl123113",
        productId="p-6edc0366-xihgkhia",
        uid="uuc9d77366u2t2j3o2",
    ):
        # 配网激活
        # 请求: device/network/devices/{device_id}/send/requestId=
        # 返回: device/network/devices/{device_id}/response/requestId=

        # device_id = str(int(time.time() * 1000))
        timestmp = str(int(time.time() * 1000))
        pus_topic = f"device/network/devices/{device_id}/send/requestId={timestmp}"
        sub_topic = f"device/network/devices/{device_id}/response/+"
        config = {
            "device": {
                "taskId": f"{uuid.uuid1()}",
                "homeId": f"{uuid.uuid1()}",
                "deviceId": f"{device_id}",
                "uuid": f"{uuid.uuid1()}",
                "productId": productId,
                "uid": uid,
                "ipaddr": "192.168.0.200",
                "devName": "test_wyk",
                "language": "CN",
                "timezone": "UTC+08",
                "serviceArea": "default_serviceArea",
                "socVer": "default_socVer",
                "mcuVer": "default_mcuVer",
                "wirelessVer": "default_wirelessVer",
                "lat": 0.0,
                "lon": 0.0,
            },
            "authKey": "default_authKey",
            "requestId": timestmp,
            "time": timestmp,
        }
        from protobuf.protobuf_py import assignNet_pb2

        device = assignNet_pb2.AssignNetRequest()
        ParseDict(config, device)
        dev_msg = device.SerializeToString()

        self.client.client_subcribe(sub_topic)
        self.client.client_publish(pus_topic, dev_msg)
        time.sleep(2)
        if self.client.last_msg:
            res = assignNet_pb2.AssignNetResponse()
            res.ParseFromString(self.client.last_msg)
            INFO.logger.info(res)

    def unbind_device(self, device_id="wyl123111"):
        """解绑设备"""
        requestId = int(time.time() * 1000)
        timestmp = requestId
        pus_topic = f"device/general_dev_to_plat/devices/{device_id}/send/{requestId}"
        sub_topic = f"device/general_dev_to_plat/devices/{device_id}/response/+"

        # 生成protobuf消息
        from protobuf.protobuf_py import unbindUser_pb2
        from protobuf.protobuf_py import generalBuffData_pb2

        request_buff = unbindUser_pb2.unbindRequest()
        request_buff.objDevId = device_id
        request_buff_serialize = request_buff.SerializeToString()

        request_protobuf = generalBuffData_pb2.GeneralBuffData()
        request_protobuf.type = CommandType.DevUnbind.value
        request_protobuf.buff = base64.b64encode(request_buff_serialize).decode()
        request_protobuf.time = timestmp
        request_protobuf.requestId = str(requestId)
        request_protobuf_serialize = request_protobuf.SerializeToString()
        # 初始化Mqtt

        # 解绑设备回调函数 ParseFromString
        def unbind_device_message(client, userdata, msg):
            INFO.logger.info(f"Received message from{msg.topic}: {msg.payload}")

            respone_data = generalBuffData_pb2.GeneralBuffData()
            respone_buff = unbindUser_pb2.unbindResponse()

            respone_data.ParseFromString(msg.payload)
            buff = base64.b64decode(respone_data.buff)
            respone_buff.ParseFromString(buff)

            INFO.logger.info(f"proto_data:\n{respone_data}")
            INFO.logger.info(f"buff_data:\n{respone_buff}")

        self.client.client_subcribe(sub_topic)
        self.client.add_topic_callback(sub_topic, unbind_device_message)
        time.sleep(2)
        # 上传消息
        self.client.client_publish(pus_topic, request_protobuf_serialize)
        time.sleep(1)

    def alarm_event_up(self, device_id="wyl123111"):
        # 请求: device/general_dev_to_plat/devices/${device_id}/send/requestId=
        # 返回: device/general_dev_to_plat/devices/${device_id}/response/requestId=

        """
        alarmType=feedSucc 代表喂食成功 alarmType=feedfail 代表喂食失败 alarmType=stuckFood 卡粮
        code =
        1.hand_feed 手动喂食消息
        2.fast_feed 快速喂食
        3.plan_feed 自动喂食(喂食计划喂食)
        成功时 value= 份数
        当code=plan_feed和成功时json={"weight": int每份总量,"time": int每天时刻, "lable": string计划名称,"quantity": int份数}
        """

        # 宠物喂食告警类型
        class AlarmType(Enum):
            FEED_SUCC = "feedSucc"
            FEED_FAIL = "feedfail"
            STUCK_FOOD = "stuckFood"

        # 宠物喂食方式类型
        class ModelCode(Enum):
            HAND_FEED = "hand_feed"
            FAST_FEED = "fast_feed"
            PLAN_FEED = "plan_feed"

        timestmp = int(time.time() * 1000)
        request_id = str(timestmp)
        pus_topic = f"device/general_dev_to_plat/devices/{device_id}/send/requestId={request_id}"
        sub_topic = f"device/general_dev_to_plat/devices/{device_id}/response/+"
        buff_config = {
            "objDevId": device_id,
            "eventId": "wyk" + str(timestmp),
            "alarmType": AlarmType.FEED_FAIL.value,
            "data": {
                "modelCode": ModelCode.FAST_FEED.value,
                "value": "2",
                "thresholdValue": "",
                "msg": "",
                # "codeType": "BOOLEAN",
                # "condition": "other",
            },
            "TmZone": "",
            "userId": "",
            "devName": "",
            "jsonInfo": "",
            "zeroTm": str(timestmp),
        }
        from protobuf.protobuf_py import devEventUp_pb2

        alarm_request_buff = devEventUp_pb2.AlarmEventVo()
        # 使用字典初始化protobuf数据
        # ParseDict(buff_config, alarm_request_buff)
        alarm_request_buff.objDevId = device_id
        alarm_request_buff.eventId = f"test_wyl{timestmp}"
        alarm_request_buff.alarmType = AlarmType.FEED_SUCC.value
        alarm_request_buff.data.modelCode = ModelCode.FAST_FEED.value
        alarm_request_buff.data.value = "2"
        alarm_request_buff.zeroTm = timestmp
        jsonInfo = {"weight": 10, "time": timestmp, "lable": "早餐", "quantity": 2}
        # alarm_request_buff.jsonInfo = str(jsonInfo)

        INFO.logger.info(f"alarm_request_buff:\n{alarm_request_buff}")
        # buf数据系列化
        alarm_request_serialize = alarm_request_buff.SerializeToString()
        # 生成设备请求数据
        data_config = {
            "type": "AlarmEventUp",
            "time": timestmp,
            "buff": base64.b64encode(alarm_request_serialize).decode(),
            "requestId": request_id,
        }
        from protobuf.protobuf_py import generalBuffData_pb2

        dev_request = generalBuffData_pb2.GeneralBuffData()

        # ParseDict(data_config, dev_request)
        dev_request.type = CommandType.AlarmEventUp.value
        dev_request.buff = base64.b64encode(alarm_request_serialize).decode()
        dev_request.time = timestmp
        dev_request.requestId = request_id
        INFO.logger.info(f"dev_request:\n{dev_request}")

        dev_request_serialize = dev_request.SerializeToString()

        # 初始化Mqtt

        # 订阅主题
        self.client.client_subcribe(sub_topic)
        # 上传消息
        self.client.client_publish(pus_topic, dev_request_serialize)
        time.sleep(2)

    def shadow_device(self, device_id="wyl123111"):
        request_id = int(time.time() * 1000)
        timestmp = int(time.time() * 1000)
        pus_topic = f"device/general_dev_to_plat/devices/{device_id}/send/requestId={request_id}"
        sub_topic = f"device/general_dev_to_plat/devices/{device_id}/response/+"

        # 初始化buff消息
        from protobuf.protobuf_py import shadowProSet_pb2

        request_buff = shadowProSet_pb2.ShadowRequest()
        request_buff.objDevId = device_id

        request_buff_serialize = request_buff.SerializeToString()

        # 初始化设备请求protobuf消息
        from protobuf.protobuf_py import generalBuffData_pb2

        dev_request = generalBuffData_pb2.GeneralBuffData()

        dev_request.type = CommandType.ShadowGet.value
        dev_request.buff = base64.b64encode(request_buff_serialize)
        dev_request.time = timestmp
        dev_request.requestId = str(request_id)
        dev_request_serialize = dev_request.SerializeToString()

        # 初始化Mqtt

        # 影子设备消息回调函数 ParseFromString
        def shadow_device_message(client, userdata, msg):
            INFO.logger.info(f"Received message from {msg.topic} : {msg.payload}")
            from protobuf.protobuf_py import generalBuffData_pb2
            from protobuf.protobuf_py import shadowProSet_pb2

            respone_data = generalBuffData_pb2.GeneralBuffData()
            respone_buff = shadowProSet_pb2.ShadowResponse()

            respone_data.ParseFromString(msg.payload)
            buff = base64.b64decode(respone_data.buff)
            respone_buff.ParseFromString(buff)

            INFO.logger.info(f"proto_data:\n{respone_data}")
            INFO.logger.info(f"buff_data:\n{respone_buff}")

        self.client.client_subcribe(sub_topic)
        self.client.add_topic_callback(sub_topic, shadow_device_message)
        time.sleep(2)
        # 上传消息
        self.client.client_publish(pus_topic, dev_request_serialize)
        time.sleep(1)


if __name__ == "__main__":
    dm = DeviceModel()
    pd = "p-379d8164-im60dioh"
    for num in range(100001, 101000):
        time.sleep(0.5)
        dm.device_activation(device_id="wyk{num}", productId=pd, uid="ox{num}")
