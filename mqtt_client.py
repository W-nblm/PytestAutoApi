import aiomqtt
from utils.logging_tool.log_control import INFO, ERROR, WARNING


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

    async def __aenter__(self):
        self.client = aiomqtt.Client(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            keepalive=self.keep_alive,
            bind_address="0.0.0.0",
        )
        # 直接返回client的上下文管理器，而不是自己调用connect/disconnect
        self._client_ctx = self.client.__aenter__()
        await self._client_ctx
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def publish(self, topic, payload):
        INFO.logger.info(f"Publishing to {topic}: {payload}")
        await self.client.publish(topic, payload)

    async def subscribe(self, topic):
        INFO.logger.info(f"Subscribing to {topic}")
        await self.client.subscribe(topic)

    def get_message_stream(self):
        return self.client.messages

    async def subscribe_many(self, topics: list[str]):
        for topic in topics:
            print(f"Subscribing to {topic}")
            await self.client.subscribe(topic)
