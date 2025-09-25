# device.py
from copy import deepcopy
from fnmatch import fnmatch
import time, uuid, asyncio
from google.protobuf.json_format import ParseDict
from protobuf.protobuf_py import (
    keeplive_pb2,
    assignNet_pb2,
    ntpTime_pb2,
    generalBuffData_pb2,
    cmdPro_pb2,
    reboot_pb2,
    shadowProSet_pb2,
    checkModel_pb2,
    devEventUp_pb2,
    birdOssEvent_pb2,
    upgradeFirmware_pb2,
    firmwareVersion_pb2,
    unbindUser_pb2,
    devEventUp_pb2,
)
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.mqtt_tool.device_events import EventFactory
from utils.mqtt_tool.mqtt_client import AsyncMqttClient
import base64
import json


class TopicRouter:
    def __init__(self):
        self._routes = []

    def add_route(self, pattern: str, handler):
        self._routes.append((pattern, handler))

    def route(self, topic: str, payload: bytes):
        for pattern, handler in self._routes:
            if fnmatch(topic, pattern):
                return handler(topic, payload)
        INFO.logger.warning(f"[Router] No handler found for topic: {topic}")


class Device:
    def __init__(self, device_id, product_id, uid, mqtt_client: AsyncMqttClient):
        self.device_id = device_id
        self.product_id = product_id
        self.uid = uid
        self.mqtt: AsyncMqttClient = mqtt_client
        self.router = TopicRouter()
        self._register_topic_handlers()

    def _register_topic_handlers(self):
        self.router.add_route(
            f"device/network/devices/{self.device_id}/response/*",
            self.handle_assign_net,
        )
        self.router.add_route(
            f"device/general_dev_to_plat/devices/{self.device_id}/response/*",
            self.handle_general_dev_to_plat_response,
        )
        self.router.add_route(
            f"device/keeplive/devices/{self.device_id}/up", self.handle_keeplive
        )
        self.router.add_route(
            f"plat/general_plat_to_dev/devices/{self.device_id}/send/*",
            self.handle_general_plat_to_dev_send,
        )
        self.router.add_route(
            f"plat/commands/home/*/devices/{self.device_id}/send/*",
            self.handle_plat_commands_response,
        )
        self.router.add_route(
            f"plat/properties_get/home/+/devices/{self.device_id}/send/*",
            self.handle_plat_properties_get_response,
        )
        self.router.add_route(
            f"device/ntp/devices/{self.device_id}/response/*",
            self.handle_ntp_response,
        )
        self.router.add_route(
            f"plat/properties/home/*/devices/{self.device_id}/report",
            self.handle_plat_properties_report,
        )
        # 更多 topic 和 handler 可以继续注册

    def handle_message(self, topic: str, payload: bytes):
        self.router.route(topic, payload)

    def handle_assign_net(self, topic: str, payload: bytes):
        msg = assignNet_pb2.AssignNetResponse()
        msg.ParseFromString(payload)
        INFO.logger.info(f"[{self.device_id}] 网络激活响应: {msg}")

    def handle_keeplive(self, topic: str, payload: bytes):
        msg = keeplive_pb2.keeplive()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic:{topic} 心跳响应: {msg}"
        )

    def handle_general_dev_to_plat_response(self, topic: str, payload: bytes):
        """自定义处理设备消息"""
        msg = generalBuffData_pb2.GeneralBuffData()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic} \n{msg}"
        )
        msg_type = [
            "FirmwareUp",
            "ShadowGet",
            "DevUnbind",
            "EventUp",
            "OssEventUp",
            "UpgradeState",
            "AlarmEventUp",
            "FirmwareUp",
            "DevLink",
            "CheckCloudPackage",
            "TelCard",
            "BirdEvent",
        ]
        if msg.type == "FirmwareUp":
            buff = base64.b64decode(msg.buff)
            firmware_msg = devEventUp_pb2.EventVo()
            firmware_msg.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] 收到平台下发固件响应: \n{firmware_msg}"
            )
        elif msg.type == "ShadowGet":
            buff = base64.b64decode(msg.buff)
            shadow_msg = shadowProSet_pb2.ShadowResponse()
            shadow_msg.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] 收到平台获取影子数据响应: \n{shadow_msg}"
            )
        elif msg.type == "DevUnbind":
            INFO.logger.info(f"[{self.device_id}] 设备解绑响应: {msg}")
        elif msg.type == "EventUp":
            buff = base64.b64decode(msg.buff)
            event_msg = devEventUp_pb2.EventVo()
            event_msg.ParseFromString(buff)
            INFO.logger.info(f"[{self.device_id}] 收到平台下发事件响应: \n{event_msg}")
        elif msg.type == "OssEventUp":
            buff = base64.b64decode(msg.buff)
            oss_msg = birdOssEvent_pb2.BirdOssEvent()
            oss_msg.ParseFromString(buff)
            INFO.logger.info(f"[{self.device_id}] 收到平台下发oss事件响应: \n{oss_msg}")
        elif msg.type == "UpgradeState":
            INFO.logger.info(f"[{self.device_id}] 收到平台下发升级状态响应: {msg}")
        elif msg.type == "AlarmEventUp":
            buff = base64.b64decode(msg.buff)
            alarm_msg = devEventUp_pb2.EventVo()
            alarm_msg.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] 收到平台下发告警事件响应: \n{alarm_msg}"
            )

    def handle_general_plat_to_dev_send(self, topic: str, payload: bytes):
        """自定义处理平台消息"""
        msg = generalBuffData_pb2.GeneralBuffData()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received from plat message on topic: {topic} \n{msg}"
        )

        type_handler_map = {
            "CheckModel": (checkModel_pb2.CheckModelRequest, "检查模型请求"),
            "UpgradeFirm": (upgradeFirmware_pb2.UpgradeRequest, "固件升级请求"),
            "FirmwareGet": (firmwareVersion_pb2.VersionRequest, "固件版本请求"),
            "AppUnbind": (unbindUser_pb2.unbindRequest, "解绑请求"),
            "Reboot": (reboot_pb2.rebootRequest, "重启请求"),
            "CloudPackage": (devEventUp_pb2.EventVo, "云端下发数据"),
            "StartPlay": (checkModel_pb2.CheckModelRequest, "开始播放指令"),
            "StoreBucket": (devEventUp_pb2.EventVo, "StoreBucket"),
            # "StopCloudPackage": None  # 不需要处理的可不写
        }

        handler = type_handler_map.get(msg.type)
        if handler:
            proto_cls, desc = handler
            buff = base64.b64decode(msg.buff)
            INFO.logger.info(f"[{self.device_id}] 收到平台下发{desc}: {buff}")
            try:
                buff_data = proto_cls()
                buff_data.ParseFromString(buff)
                INFO.logger.info(f"[{self.device_id}] 解析结果: \n{buff_data}")
            except Exception as e:
                ERROR.logger.error(f"[{self.device_id}] 解析{msg.type}失败: {e}")
        elif msg.type == "StopCloudPackage":
            INFO.logger.info(f"[{self.device_id}] 收到平台下发停止云端下发数据指令")
        else:
            INFO.logger.warning(f"[{self.device_id}] 未知消息类型: {msg.type}")

    def handle_plat_commands_response(self, topic: str, payload: bytes):
        """自定义处理平台命令响应"""
        # msg = cmdPro_pb2.CmdProResponse()
        # msg.ParseFromString(payload)
        msg = cmdPro_pb2.CmdProRequest()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic} \n{msg}"
        )

    def handle_plat_properties_get_response(self, topic: str, payload: bytes):
        """自定义处理平台属性获取响应"""
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic}, payload: {payload}"
        )

    def handle_plat_properties_report(self, topic: str, payload: bytes):
        """自定义处理平台属性上报"""
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic}, payload: {payload}"
        )

        msg = cmdPro_pb2.CmdProResponse()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic} \n{msg}"
        )

    def handle_ntp_response(self, topic: str, payload: bytes):
        """自定义处理ntp响应"""
        # 等待接收绑定设备的推送消息、反序列化收到推送消息
        deviceRecvTime = int(time.time() * 1000)
        ntpResponse = ntpTime_pb2.NtpRespose()
        ntpResponse.ParseFromString(payload)
        response = {
            "deviceSendTime": ntpResponse.deviceSendTime,
            "serverRecvTime": ntpResponse.serverRecvTime,
            "serverSendTime": ntpResponse.serverSendTime,
        }
        devtime = (
            response["serverRecvTime"]
            + response["serverSendTime"]
            + deviceRecvTime
            - response["deviceSendTime"]
        ) / 2
        INFO.logger.info(f"服务器响ntp反序列化后数据:{response}")
        INFO.logger.info(f"服务端unix时间: {devtime}")

    def get_topics(self) -> list[str]:
        """返回该设备需要订阅的所有 topic"""
        return [
            f"plat/general_plat_to_dev/devices/{self.device_id}/send/+",
            f"device/general_dev_to_plat/devices/{self.device_id}/response/+",
            f"device/network/devices/{self.device_id}/response/+",
            f"device/ntp/devices/{self.device_id}/response/+",
            f"plat/commands/home/0/devices/{self.device_id}/send/+",
            f"plat/properties_get/home/0/devices/{self.device_id}/send/+",
            f"plat/properties/home/0/devices/{self.device_id}/report",
        ]

    async def send_heartbeat(self):
        """发送心跳包"""
        topic = f"device/keeplive/devices/{self.device_id}/up"
        msg = keeplive_pb2.keeplive()
        msg.objDevId = self.device_id
        msg.status = 1
        msg.time = int(time.time() * 1000)
        msg = msg.SerializeToString()
        INFO.logger.info(f"[{self.device_id}] Sending heartbeat message: {msg}")
        await self.mqtt.publish(topic, msg)

    async def run_keeplive_loop(self):
        while True:
            await self.send_heartbeat()
            await asyncio.sleep(300)

    async def property_report_loop(self):
        """
        设备属性上报循环
        """
        INFO.logger.info(f"[{self.device_id}] Starting property report loop...")
        topic = f"plat/properties/home/0/devices/{self.device_id}/report"
        from google.protobuf.json_format import ParseDict

        template_data = {
            "result": True,
            "objDevId": self.device_id,
            "msg": "wyk test",
            "productId": self.product_id,
            "optype": cmdPro_pb2.opType.Property,
            "data": {"code": "basic_indicator", "type": "INTEGER", "value": "6"},
        }
        data_list = {
            "temperature_mark_sw": {"value": "0", "time": "1755155339425"},
            "pir_step": {"type": "ENUM", "value": "1", "time": "1755155339473"},
            "time_watermark": {"type": "ENUM", "value": "2", "time": "1755155339444"},
            "infrared_sw": {"value": "1", "time": "1755155339461"},
            "charge_status": {"value": "0", "time": "1755155348632"},
            "sd_capacity": {
                "type": "JSON",
                "value": '{"unit": "M","total": 8192,"current": 888}',
                "time": "1755155339538",
            },
            "sd_status": {"type": "ENUM", "value": "1", "time": "1755155339534"},
            "wifi_signal": {"type": "INTEGER", "value": "-23", "time": "1755155348669"},
            "sd_formatting": {"value": "1", "time": "1755074741696"},
            "feed_plan_sw": {"value": "1", "time": "1755155339495"},
            "force_retreat_sw": {"value": "1", "time": "1755155339482"},
            "detect_person_switch": {"value": "1", "time": "1755155339499"},
            "volume_set": {"type": "INTEGER", "value": "48", "time": "1755155339462"},
            "feed_plan": {
                "type": "JSON",
                "value": '{"weight":12,"feedPlans":[{"time":750,"label":"","quantity":1}]}',
                "time": "1755155339499",
            },
            "battery_quantity": {
                "type": "INTEGER",
                "value": "10",
                "time": "1755155348664",
            },
            "anti_flicker": {"type": "ENUM", "value": "0", "time": "1755155339413"},
            "detect_time": {"type": "ENUM", "value": "30", "time": "1755155339483"},
            "rt_v_bird_quality": {
                "type": "ENUM",
                "value": "0",
                "time": "1755155339427",
            },
            "basic_osd": {"value": "1", "time": "1755155339435"},
            "basic_indicator": {"value": "1", "time": "1755155339443"},
        }

        def build_protobuf_list(template_data, data_list, default_type="STRING"):
            """
            批量生成 protobuf 对象

            :param proto_cls: protobuf 类,比如 cmdPro_pb2.CmdProResponse
            :param template_data: dict 模板,包含基础固定字段
            :param data_list: dict 数据列表,key=code,value=dict(字段信息)
            :param default_type: 如果 data 中没有 type 字段,使用的默认值
            :return: list[proto_cls]
            """
            proto_objects = {}
            for code, detail in data_list.items():
                # 深拷贝模板,避免相互影响
                data_dict = deepcopy(template_data)
                # 修改 data 部分
                data_dict["data"]["code"] = code
                data_dict["data"]["type"] = detail.get("type", default_type)
                data_dict["data"]["value"] = detail["value"]
                try:
                    INFO.logger.info(f"[{self.device_id}] 准备上报属性: {data_dict}")
                    proto_obj = cmdPro_pb2.CmdProResponse()
                    ParseDict(data_dict, proto_obj)
                    proto_obj_serialize = proto_obj.SerializeToString()
                    proto_objects[code] = proto_obj_serialize
                    INFO.logger.info(
                        f"[{self.device_id}] 构造 protobuf 对象: {proto_obj}"
                    )
                except Exception as e:
                    INFO.logger.error(
                        f"[{self.device_id}] 构造 protobuf 对象失败: {e}", exc_info=True
                    )

            return proto_objects

        proto_list = build_protobuf_list(template_data, data_list)

        INFO.logger.info(proto_list)

        return topic, proto_list
        # request_protobuf = cmdPro_pb2.CmdProResponse()
        # request_protobuf.result = 1
        # request_protobuf.objDevId = self.device_id
        # request_protobuf.productId = self.product_id
        # request_protobuf.optype = cmdPro_pb2.opType.Property
        # request_protobuf.data.code = "battery_quantity"
        # request_protobuf.data.type = cmdPro_pb2.modelType__pb2.ModelType.INTEGER
        # request_protobuf.data.value = "6"
        # request_protobuf.authKey = ""
        # request_protobuf.requestId = self.device_id

        # request_protobuf_serialize = request_protobuf.SerializeToString()

    async def run_property_report_loop(self):
        """
        循环上报设备属性
        """
        topic, proto_list = await self.property_report_loop()
        while True:
            for proto_obj_serialize in proto_list.values():
                await self.mqtt.publish(topic, proto_obj_serialize)
                INFO.logger.info(f"[{self.device_id}] 上报属性")
                await asyncio.sleep(1)
            await asyncio.sleep(300)

    async def run_single_property_report_loop(self, code):
        """
        上传单个属性
        """
        topic, proto_list = await self.property_report_loop()
        proto_obj_serialize = proto_list[code]
        while True:
            await self.mqtt.publish(topic, proto_obj_serialize)
            INFO.logger.info(f"[{self.device_id}] 上报属性")
            await asyncio.sleep(10)

    async def device_to_plat_loop(self):
        """ "
        设备主动向平台发送消息循环
        命令类型:
        FirmwareUp:设备上传固件版本;
        ShadowGet:设备主动获取一需要更新的影子设备属性;
        DevUnbind:设备主动请求解绑,
        EventUp:普通事件上报（只上传图片）,
        OssEventUp:云事件上报（上报需要开通云存储功能）,
        UpgradeState:升级固件状态上报.
        AlarmEventUp:告警事件上报;
        FirmwareUp:固件版本主动上报;
        DevLink:设备休眠后开始连接,代表设备从休眠开始上线
        CheckCloudPackage:设备在套餐快过期时主动请求后台获取是否有新套餐信息
        TelCard:上传4g卡消息
        """
        INFO.logger.info(f"[{self.device_id}] Starting device to plat loop...")
        buff_type_list = [
            "FirmwareUp",
            "ShadowGet",
            "DevUnbind",
            "EventUp",
            "OssEventUp",
            "UpgradeState",
            "AlarmEventUp",
            "DevLink",
            "CheckCloudPackage",
            "TelCard",
            "BirdEvent",
        ]

        def random_event_id():
            random_str = uuid.uuid4().hex  # 生成32字符十六进制
            part1, part2 = random_str[:6], random_str[6:17]  # 拆分前6位和后续11位
            return f"d-{part1}-{part2}"

        topic = f"device/general_dev_to_plat/devices/{self.device_id}/send/requestId="

        while True:
            # for event_type in buff_type_list:
            try:
                event_type = "BirdEvent"
                event_obj = EventFactory.create_event(event_type, self.device_id)
                protobuf_data = event_obj.generate()

                await self.mqtt.publish(topic, protobuf_data)
                INFO.logger.info(f"[{self.device_id}] Sent {event_type} event")

                await asyncio.sleep(300)
            except Exception as e:
                INFO.logger.error(
                    f"[{self.device_id}] Error occurred while sending {event_type} event: {e}",
                    exc_info=True,
                )

    async def activate(self):
        ts = str(int(time.time() * 1000))
        topic = f"device/network/devices/{self.device_id}/send/requestId="
        INFO.logger.info(f"[{self.device_id}] Activating...")

        msg = assignNet_pb2.AssignNetRequest()
        ParseDict(
            {
                "device": {
                    "taskId": f"{uuid.uuid1()}",
                    "homeId": f"{uuid.uuid1()}",
                    "deviceId": f"{self.device_id}",
                    "uuid": f"{uuid.uuid1()}",
                    "productId": f"{self.product_id}",
                    "uid": f"{self.uid}",
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
                "requestId": "requestId=",
                "time": ts,
            },
            msg,
        )
        await self.mqtt.publish(topic, msg.SerializeToString())
