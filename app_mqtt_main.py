import asyncio
import sys
from app_mqtt_manager import AppMqttManager
from utils.mqtt_tool.mqtt_client import AsyncMqttClient


async def listen_for_messages(manager: AppMqttManager):
    async for msg in manager.mqtt.get_message_stream():
        topic = str(msg.topic)
        payload = msg.payload
        if manager.user_id in topic:
            manager.handle_message(topic, payload)


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    mqtt_client = AsyncMqttClient()
    await mqtt_client.connect()

    app_mgr = AppMqttManager(user_id="uub197c66706beq0qc", mqtt_client=mqtt_client)
    await app_mgr.subscribe_all()

    asyncio.create_task(listen_for_messages(app_mgr))
    
    try:
        while True:
            await asyncio.sleep(30)
    except KeyboardInterrupt:
        await mqtt_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
