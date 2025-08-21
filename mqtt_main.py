import sys
from utils.logging_tool.log_control import INFO, ERROR, WARNING
import asyncio
import sys
from utils.mqtt_tool.device_manager import DeviceManager

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    manager = DeviceManager()
    devices = [
        # {
        #     "device_id": "d-8d8b4768-ns6aoiho",
        #     "product_id": "p-0c947c67-8ghjjvw3",
        #     "uid": "uub197c66706beq0qc",
        #     "activate": False,
        #     "start_tasks": False,
        # },
        {
            "device_id": "d-8d8b4768-ns6aoi66",
            "product_id": "p-0c947c67-8ghjjvw3",
            "uid": "uub197c66706beq0qc",
            "activate": False,
            "start_tasks": True,
        },
    ]
    # 创建多个设备并添加到管理器中
    await manager.start(device_configs=devices)

    try:
        while True:
            await asyncio.sleep(60)
            manager.list_status()
    except (KeyboardInterrupt, asyncio.CancelledError):
        await manager.stop_all()


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
