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
                    print(f"  特征: {char.uuid} | 属性: {props}")

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def write_data(self, data: bytes, response: bool = True):
        if self.client:
            await self.client.write_gatt_char(
                self.write_char_uuid, data, response=response
            )

    async def start_notify(self, callback: Callable):
        if self.client:
            await self.client.start_notify(self.notify_char_uuid, callback)

    async def stop_notify(self):
        if self.client:
            await self.client.stop_notify(self.notify_char_uuid)
