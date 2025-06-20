from utils.mqtt_tool.devices import DeviceModel
from utils.mqtt_tool.mqtt import Mqtt
import sys
from utils.redis_tool.redis_helper import RedisHelper
from utils.mysql_tool.mysql_tool import MysqlTool
from utils.logging_tool.log_control import INFO, ERROR, WARNING

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
import asyncio
import sys
from mqtt_client import AsyncMqttClient
from device import Device

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():

    async with AsyncMqttClient() as mqtt_client:
        # 初始化device
        INFO.logger.info("初始化device")
        devices = [
            Device(
                device_id=f"dev{i:03d}",
                product_id="p-0c947c67-8ghjjvw3",
                uid="uub197c66706beq0qc",
                mqtt_client=mqtt_client,
            )
            for i in range(2)
        ]
        all_topics = []
        for device in devices:
            all_topics.extend(device.get_topics())
        await mqtt_client.subscribe_many(all_topics)
        # ✅ 并发激活所有设备

        INFO.logger.info("激活所有设备...")
        await asyncio.gather(*(device.activate() for device in devices))

        # 监听消息流
        async for message in mqtt_client.get_message_stream():
            topic_str = str(message.topic)  
            payload = message.payload
            for device in devices:
                if device.device_id in topic_str:
                    device.handle_message(topic_str, payload)

        await asyncio.gather(*(device.stop() for device in devices))


if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == "__main__":
#     # 获取用户的uid，用户邮箱：834532523@qq.com
#     # 初始化mysql
#     mysql_tool = MysqlTool(
#         host="47.107.113.31",
#         user="iot_test",
#         port=13306,
#         password="DPbbkXGvauYD38uY",
#         database="iot-cloud",
#     )
#     # 获取用户的uid
#     user_data = mysql_tool.query(
#         "select au.user_uid FROM app_user au WHERE au.email = '834532523@qq.com' AND au.reg_app_source = 'WObird'",
#         state="one",
#     )
#     INFO.logger.info(user_data)  # {'user_uid': 'uub197c66706beq0qc'}

#     # 获取用户下的设备
#     data = mysql_tool.query(
#         f'select * from device_app_user_ship ds where ds.user_id = "{user_data["user_uid"]}"'
#     )
#     INFO.logger.info(data)
