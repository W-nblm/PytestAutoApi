# main.py

import asyncio
from utils.ble.packet_utils import json_to_binary_packets, parse_packet
from utils.ble.ble_client import BLEClient

SERVICE_UUID = "0000181c-0000-1000-8000-00805f9b34fb"
WRITE_CHAR_UUID = "00002a8a-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR_UUID = "00002a90-0000-1000-8000-00805f9b34fb"


def notification_handler(sender, data):
    parsed = parse_packet(data)
    print(f"接收到数据: {parsed}")


async def main():
    ble_client = BLEClient(SERVICE_UUID, WRITE_CHAR_UUID, NOTIFY_CHAR_UUID)

    print("🔍 正在扫描设备...")
    devices = await ble_client.scan_devices(name_prefix="wobirdy")
    if not devices:
        print("❌ 未找到设备")
        return

    for idx, device in enumerate(devices):
        print(f"{idx}: {device.name} [{device.address}]")

    index = int(input("请选择设备编号: "))
    if index < 0 or index >= len(devices):
        print("❌ 无效的设备编号")
        return

    selected_device = devices[index]
    if not await ble_client.connect(selected_device.address):
        print("❌ 连接失败")
        return
    print("✅ 连接成功")

    # 获取服务和特征值
    await ble_client.get_services()

    # 开始监听通知
    await ble_client.start_notify(notification_handler)

    json_str = {
        "timeZone": "+8:00",
        "dataCenterCode": "AL",
        "language": "CN",
        "productId": "p-",
        "userId": "uub197c66706beq0qc",
        "ssid": "test",
        "pwd": "w12345678",
        "taskid": "21ff2308bc914eb",
    }

    command = 0x01
    packets = json_to_binary_packets(str(json_str), command)
    for packet in packets:
        await ble_client.write_data(packet, response=True)

    print("发送数据成功")

    await asyncio.sleep(10)
    await ble_client.stop_notify()
    await ble_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
