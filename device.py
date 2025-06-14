# device.py
import time, uuid, asyncio
from google.protobuf.json_format import ParseDict
from protobuf.protobuf_py import keeplive_pb2, assignNet_pb2


class Device:
    def __init__(self, device_id, product_id, uid, mqtt_client):
        self.device_id = device_id
        self.product_id = product_id
        self.uid = uid
        self.mqtt = mqtt_client

    def get_topics(self) -> list[str]:
        """返回该设备需要订阅的所有 topic"""
        return [
            f"plat/general_plat_to_dev/devices/{self.device_id}/send/+",
            f"device/general_dev_to_plat/devices/{self.device_id}/response/+",
            f"device/network/devices/{self.device_id}/response/+",
            f"device/ntp/devices/{self.device_id}/response/+",
            f"plat/commands/home/+/devices/{self.device_id}/send/+",
            f"plat/properties_get/home/+/devices/{self.device_id}/send/+",
        ]

    def handle_message(self, topic: str, payload: bytes):
        """自定义逻辑处理接收到的消息"""
        print(f"[{self.device_id}] Received message on {topic}: {payload.decode()}")

    async def send_heartbeat(self):
        topic = f"device/keeplive/devices/{self.device_id}/up"
        msg = keeplive_pb2.keeplive(
            objDevId=self.device_id, status=1, time=int(time.time() * 1000)
        ).SerializeToString()
        await self.mqtt.publish(topic, msg)

    async def activate(self):
        ts = str(int(time.time() * 1000))
        topic = f"device/network/devices/{self.device_id}/send/requestId="
        resp_topic = f"device/network/devices/{self.device_id}/response/+"
        print(f"[{self.device_id}] Activating...")
        await self.mqtt.subscribe(resp_topic)

        msg = assignNet_pb2.AssignNetRequest()
        ParseDict(
            {
                "device": {
                    "deviceId": self.device_id,
                    "productId": self.product_id,
                    "uid": self.uid,
                    "taskId": str(uuid.uuid4()),
                    "homeId": str(uuid.uuid4()),
                    "uuid": str(uuid.uuid4()),
                    "ipaddr": "127.0.0.1",
                },
                "authKey": "xxx",
                "requestId": ts,
                "time": ts,
            },
            msg,
        )
        await self.mqtt.publish(topic, msg.SerializeToString())

    async def run_keeplive_loop(self):
        while True:
            await self.send_heartbeat()
            await asyncio.sleep(60)
