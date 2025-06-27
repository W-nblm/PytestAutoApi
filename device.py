# device.py
from fnmatch import fnmatch
import time, uuid, asyncio
from google.protobuf.json_format import ParseDict
from protobuf.protobuf_py import (
    keeplive_pb2,
    assignNet_pb2,
    ntpTime_pb2,
    generalBuffData_pb2,
    cmdPro_pb2,
    shadowProSet_pb2,
    checkModel_pb2,
    devEventUp_pb2,
    birdOssEvent_pb2,
)
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from mqtt_client import AsyncMqttClient
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
            self.handle_general_plat_to_dev_response,
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
        if msg.type == "ShadowGet":
            buff = base64.b64decode(msg.buff)
            shadow_msg = shadowProSet_pb2.ShadowResponse()
            shadow_msg.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] 收到平台获取影子数据响应: \n{shadow_msg}"
            )

    def handle_general_plat_to_dev_response(self, topic: str, payload: bytes):
        """自定义处理平台消息"""
        msg = generalBuffData_pb2.GeneralBuffData()
        msg.ParseFromString(payload)
        INFO.logger.info(
            f"[{self.device_id}] Received message on topic: {topic} \n{msg}"
        )
        if msg.type == "CloudPackage":
            buff = base64.b64decode(msg.buff)
            INFO.logger.info(f"[{self.device_id}] 收到云端下发数据: {buff}")
            buff_data = devEventUp_pb2.EventVo()
            buff_data.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] Received message on topic: {topic} \n{buff_data}"
            )
        if msg.type == "StartPlay":
            buff = base64.b64decode(msg.buff)
            INFO.logger.info(f"[{self.device_id}] 收到平台下发开始播放指令: {buff}")
            buff_data = checkModel_pb2.CheckModelRequest()
            buff_data.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] Received message on topic: {topic} \n{buff_data}"
            )
        if msg.type == "StoreBucket":
            buff = base64.b64decode(msg.buff)
            INFO.logger.info(f"[{self.device_id}] 收到平台下发StoreBucket: {buff}")
            buff_data = devEventUp_pb2.EventVo()
            buff_data.ParseFromString(buff)
            INFO.logger.info(
                f"[{self.device_id}] Received message on topic: {topic} \n{buff_data}"
            )

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
            f"plat/commands/home/+/devices/{self.device_id}/send/+",
            f"plat/properties_get/home/+/devices/{self.device_id}/send/+",
            f"plat/properties/home/+/devices/{self.device_id}/report",
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
            await asyncio.sleep(60)

    async def property_report_loop(self):

        topic = f"plat/properties/home/+/devices/{self.device_id}/report"
        request_protobuf = cmdPro_pb2.CmdProResponse()
        request_protobuf.result = 1
        request_protobuf.objDevId = self.device_id
        request_protobuf.msg = "wyk test"
        request_protobuf.productId = self.product_id
        request_protobuf.optype = cmdPro_pb2.opType.Property
        request_protobuf.data.code = "basic_indicator"
        request_protobuf.data.type = cmdPro_pb2.modelType__pb2.ModelType.INTEGER
        request_protobuf.data.value = "6"

        request_protobuf_serialize = request_protobuf.SerializeToString()
        INFO.logger.info(f"[{self.device_id}] 上报属性")
        await self.mqtt.publish(topic, request_protobuf_serialize)

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


