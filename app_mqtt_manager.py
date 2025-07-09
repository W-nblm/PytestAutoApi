from utils.logging_tool.log_control import INFO, WARNING
from mqtt_client import AsyncMqttClient
import asyncio
import json


class TopicRouter:
    def __init__(self):
        self.routes = []

    def add_route(self, pattern, handler):
        self.routes.append((pattern, handler))

    def route(self, topic: str, payload: bytes):
        for pattern, handler in self.routes:
            if pattern in topic:
                return handler(topic, payload)
        WARNING.logger.warning(f"[Router] 无 handler 匹配: {topic}")


class AppMqttManager:
    def __init__(self, user_id: str, mqtt_client: AsyncMqttClient):
        self.user_id = user_id
        self.mqtt = mqtt_client
        self.router = TopicRouter()
        self._register_routes()

    def _register_routes(self):
        self.router.add_route(
            f"app/message/{self.user_id}/down", self.handle_app_to_plat
        )
        self.router.add_route(f"app/keeplive/{self.user_id}/send", self.handle_keeplive)
        self.router.add_route(
            f"plat/message/{self.user_id}/send", self.handle_plat_to_app
        )
        self.router.add_route(f"plat/alarm/{self.user_id}/send", self.handle_alarm)
        self.router.add_route(
            f"plat/detect/{self.user_id}/send", self.handle_detect_event
        )

    async def subscribe_all(self):
        topics = [
            f"app/message/{self.user_id}/down",
            f"app/keeplive/{self.user_id}/send",
            f"plat/message/{self.user_id}/send",
            f"plat/alarm/{self.user_id}/send",
            f"plat/detect/{self.user_id}/send",
        ]
        await self.mqtt.subscribe_many(topics)

    def handle_message(self, topic: str, payload: bytes):
        self.router.route(topic, payload)

    def handle_app_to_plat(self, topic: str, payload: bytes):
        INFO.logger.info(f"[{self.user_id}] App发给平台: topic={topic}, msg={payload}")

    def handle_keeplive(self, topic: str, payload: bytes):
        INFO.logger.info(f"[{self.user_id}] App心跳: topic={topic}, msg={payload}")

    def handle_plat_to_app(self, topic: str, payload: bytes):
        INFO.logger.info(
            f"[{self.user_id}] 平台消息发给App: topic={topic}, msg={payload}"
        )

    def handle_alarm(self, topic: str, payload: bytes):
        INFO.logger.info(f"[{self.user_id}] 告警消息: topic={topic}, msg={payload}")

    def handle_detect_event(self, topic: str, payload: bytes):
        INFO.logger.info(f"[{self.user_id}] 检测事件: topic={topic}, msg={payload}")

    async def send_message_to_app(self, content: str):
        topic = f"plat/message/{self.user_id}/send"
        await self.mqtt.publish(topic, content.encode())

    async def send_alarm_to_app(self, alarm: dict):
        topic = f"plat/alarm/{self.user_id}/send"
        await self.mqtt.publish(topic, json.dumps(alarm).encode())

    async def send_detect_event(self, event: dict):
        topic = f"plat/detect/{self.user_id}/send"
        await self.mqtt.publish(topic, json.dumps(event).encode())


class AppMqttManagerPool:
    def __init__(self, mqtt_client: AsyncMqttClient):
        self.mqtt = mqtt_client
        self.managers: dict[str, AppMqttManager] = {}
        self._listen_task: asyncio.Task | None = None

    async def add_user(self, user_id: str):
        if user_id in self.managers:
            INFO.logger.info(f"[{user_id}] 已存在，跳过")
            return

        manager = AppMqttManager(user_id=user_id, mqtt_client=self.mqtt)
        await manager.subscribe_all()
        self.managers[user_id] = manager
        INFO.logger.info(f"[{user_id}] 已订阅")

    async def start_listening(self):
        self._listen_task = asyncio.create_task(self._listen_loop())

    async def _listen_loop(self):
        async for msg in self.mqtt.get_message_stream():
            topic = str(msg.topic)
            payload = msg.payload
            matched = False
            for uid, manager in self.managers.items():
                if uid in topic:
                    manager.handle_message(topic, payload)
                    matched = True
                    break
            if not matched:
                WARNING.logger.warning(f"无人匹配该topic: {topic}")

    def get_user_manager(self, user_id: str) -> AppMqttManager | None:
        return self.managers.get(user_id)

    async def stop(self):
        if self._listen_task:
            self._listen_task.cancel()
            await asyncio.gather(self._listen_task, return_exceptions=True)
            INFO.logger.info("MQTT 消息监听已停止")
