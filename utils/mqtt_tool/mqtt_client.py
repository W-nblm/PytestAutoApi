import asyncio
import aiomqtt
from utils.logging_tool.log_control import INFO, ERROR


class AsyncMqttClient:
    def __init__(
        self,
        hostname="47.107.113.31",
        port=16883,
        username="iot",
        password="Lzy#iot",
        keep_alive=600,
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.keep_alive = keep_alive
        self.client = None
        self._client_ctx = None
        self._connected = False

    async def connect(self):
        """显式连接方法（适合长期运行）"""
        if self._connected:
            INFO.logger.warning("MQTT client already connected.")
            return

        self.client = aiomqtt.Client(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            keepalive=self.keep_alive,
            bind_address="0.0.0.0",
        )
        self._client_ctx = self.client.__aenter__()
        await self._client_ctx
        self._connected = True
        INFO.logger.info("✅ MQTT connected.")

    async def disconnect(self):
        """断开连接"""
        if self.client and self._connected:
            await self.client.__aexit__(None, None, None)
            self._connected = False
            INFO.logger.info("🛑 MQTT disconnected.")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def publish(self, topic, payload):
        if not self._connected:
            ERROR.logger.error(f"MQTT not connected. Cannot publish to {topic}")
            return
        INFO.logger.info(f"📤 Publishing to {topic}: {payload}")
        if isinstance(payload, list):
            for p in payload:
                await self.client.publish(topic, p)
                await asyncio.sleep(0.2)
        else:
            await self.client.publish(topic, payload)

    async def subscribe(self, topic):
        if not self._connected:
            ERROR.logger.error(f"MQTT not connected. Cannot subscribe to {topic}")
            return
        INFO.logger.info(f"📥 Subscribing to {topic}")
        await self.client.subscribe(topic)

    async def subscribe_many(self, topics: list[str]):
        for topic in topics:
            await self.subscribe(topic)

    def get_message_stream(self):
        if not self._connected:
            ERROR.logger.error("MQTT not connected. Cannot get message stream.")
            return None
        return self.client.messages
