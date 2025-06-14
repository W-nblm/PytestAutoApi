# device_manager.py
import asyncio
from device import Device

class DeviceManager:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.devices = []

    def add_device(self, device_id, product_id, uid):
        device = Device(device_id, product_id, uid, self.mqtt_client)
        self.devices.append(device)

    async def start_all(self):
        await asyncio.gather(*(d.activate() for d in self.devices))
        for d in self.devices:
            asyncio.create_task(d.run_keeplive_loop())
