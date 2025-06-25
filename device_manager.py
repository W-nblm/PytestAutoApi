import asyncio
from device import Device
from mqtt_client import AsyncMqttClient
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from typing import List


class DeviceManager:
    def __init__(self):
        self.devices: list[Device] = []
        self.tasks: dict[str, list[asyncio.Task]] = {}
        self.mqtt_client: AsyncMqttClient = AsyncMqttClient()
        self._mqtt_listener_task: asyncio.Task | None = None

    async def start(self, device_configs: list[dict]):
        """初始化所有设备并启动消息监听"""
        await self.mqtt_client.connect()
        for cfg in device_configs:
            device = Device(
                device_id=cfg["device_id"],
                product_id=cfg["product_id"],
                uid=cfg["uid"],
                mqtt_client=self.mqtt_client,
            )
            await self.add_device(
                device, activate=cfg["activate"], start_tasks=cfg["start_tasks"]
            )

        self._mqtt_listener_task = asyncio.create_task(self._mqtt_message_listener())

    async def add_device(self, device, activate=True, start_tasks=True):
        """添加设备，可控制是否激活和启动后台任务"""
        self.devices.append(device)
        self.tasks[device.device_id] = []

        try:
            for topic in device.get_topics():
                await device.mqtt.subscribe(topic)
                INFO.logger.info(f"[{device.device_id}] 订阅 topic: {topic}")
        except Exception as e:
            ERROR.logger.error(f"[{device.device_id}] 订阅 topic 失败: {e}")

        if activate:
            try:
                await device.activate()
                INFO.logger.info(f"[{device.device_id}] 激活完成")
            except Exception as e:
                ERROR.logger.error(f"[{device.device_id}] 激活失败: {e}")

        if start_tasks:
            try:
                t1 = asyncio.create_task(device.run_keeplive_loop())
                t2 = asyncio.create_task(device.property_report_loop())
                self.tasks[device.device_id].extend([t1, t2])
                INFO.logger.info(f"[{device.device_id}] 后台任务已启动")
            except Exception as e:
                ERROR.logger.error(f"[{device.device_id}] 启动任务失败: {e}")

    async def _mqtt_message_listener(self):
        """内部：启动消息监听任务，并分发到设备"""
        try:
            async for message in self.mqtt_client.get_message_stream():
                topic_str = str(message.topic)
                payload = message.payload

                matched = False
                for device in self.devices:
                    if device.device_id in topic_str:
                        try:
                            device.handle_message(topic_str, payload)
                        except Exception as e:
                            ERROR.logger.exception(
                                f"[{device.device_id}] 消息处理异常: {e}"
                            )
                        matched = True
                        break
                if not matched:
                    WARNING.logger.warning(f"未找到设备处理 topic: {topic_str}")

        except Exception as e:
            ERROR.logger.exception(f"MQTT 消息监听出错: {e}")

    async def activate_all(self):
        """激活所有设备"""
        for device in self.devices:
            INFO.logger.info(f"[{device.device_id}] 开始激活")
            try:
                await device.activate()
                INFO.logger.info(f"[{device.device_id}] 激活完成")
            except Exception as e:
                ERROR.logger.error(f"[{device.device_id}] 激活失败: {e}")

    async def start_all(self):
        """启动所有设备的后台任务"""
        for device in self.devices:
            try:
                INFO.logger.info(f"[{device.device_id}] 启动心跳/上报任务")

                t1 = asyncio.create_task(device.run_keeplive_loop())
                t2 = asyncio.create_task(device.property_report_loop())

                self.tasks[device.device_id].extend([t1, t2])
            except Exception as e:
                ERROR.logger.error(f"[{device.device_id}] 启动任务失败: {e}")

        INFO.logger.info("✅ 所有设备任务已启动")

    async def stop_all(self):
        """统一关闭所有后台任务和 MQTT 客户端"""
        for task_list in self.tasks.values():
            for task in task_list:
                task.cancel()
        await asyncio.gather(
            *(t for task_group in self.tasks.values() for t in task_group),
            return_exceptions=True,
        )
        if self._mqtt_listener_task:
            self._mqtt_listener_task.cancel()
            await asyncio.gather(self._mqtt_listener_task, return_exceptions=True)

        await self.mqtt_client.disconnect()
        INFO.logger.info("✅ 所有任务和 MQTT 客户端已关闭")

    def list_status(self):
        """列出当前管理的设备和任务状态"""
        for device in self.devices:
            task_list = self.tasks.get(device.device_id, [])
            statuses = [
                f"cancelled={t.cancelled()}, done={t.done()}" for t in task_list
            ]
            INFO.logger.info(f"[{device.device_id}] 当前任务状态: {statuses}")
