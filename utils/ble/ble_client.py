# ble_client.py

import asyncio
from bleak import BleakScanner, BleakClient
from typing import List, Callable


class BLEClient:
    def __init__(self, service_uuid: str, write_char_uuid: str, notify_char_uuid: str):
        self.service_uuid = service_uuid
        self.write_char_uuid = write_char_uuid
        self.notify_char_uuid = notify_char_uuid
        self.client = None
        self.read_char_uuid = []

    async def scan_devices(self, name_prefix: str = "") -> List:
        devices = await BleakScanner.discover(timeout=5.0)
        if name_prefix:
            devices = [d for d in devices if d.name and d.name.startswith(name_prefix)]
        return devices

    async def connect(self, address: str) -> bool:
        self.client = BleakClient(address)
        try:
            await self.client.connect()
            return self.client.is_connected
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    async def get_services(self):
        if self.client:
            print("🔍 正在发现服务和特征...")
            services = self.client.services
            for service in services:
                print(f"服务: {service.uuid}")
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"  特性 UUID: {char.uuid}")
                    print(f"    句柄: {char.handle}")
                    print(f"    属性: {char.properties}")
                    print(f"    描述: {char.description}")
                    print("    ---")
                    if props == "read":
                        self.read_char_uuid.append(
                            {"desc": char.description, "uuid": char.uuid}
                        )

    async def read_data(self):
        if self.client:
            for char in self.read_char_uuid:
                if char.get("desc") == "Appearance":
                    value = await self.client.read_gatt_char(char.get("uuid"))
                    value = int.from_bytes(value, byteorder="little")
                    print(f"uuid:{char} 读取到数据: {value}")
                elif char.get("desc") == "Peripheral Preferred Connection Parameters":
                    value = await self.client.read_gatt_char(char.get("uuid"))
                    min_interval = int.from_bytes(value[0:2], byteorder="little")
                    max_interval = int.from_bytes(value[2:4], byteorder="little")
                    slave_latency = int.from_bytes(value[4:6], byteorder="little")
                    timeout = int.from_bytes(value[6:8], byteorder="little")
                    print(
                        f"uuid:{char} 读取到数据: Min Interval: {min_interval}, Max Interval: {max_interval}, Slave Latency: {slave_latency}, Timeout: {timeout}"
                    )
                else:
                    value = await self.client.read_gatt_char(char.get("uuid"))
                    print(f"uuid:{char} 读取到数据: {value}")

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def write_data(self, data: bytes, response: bool = True):
        if self.client:
            await self.client.write_gatt_char(
                self.write_char_uuid, data, response=response
            )
            print(f"已发送数据: {data}")

    async def start_notify(self, callback: Callable):
        if self.client:
            await self.client.start_notify(self.notify_char_uuid, callback)

    async def stop_notify(self):
        if self.client:
            await self.client.stop_notify(self.notify_char_uuid)
