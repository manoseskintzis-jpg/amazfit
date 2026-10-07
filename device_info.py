import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"

async def main():
    async with BleakClient(ADDRESS) as client:
        # Serial Number characteristic
        serial = await client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")
        # Firmware Revision characteristic
        firmware = await client.read_gatt_char("00002a28-0000-1000-8000-00805f9b34fb")
        
        print(f"Serial Number: {serial.decode('utf-8')}")
        print(f"Firmware:      {firmware.decode('utf-8')}")

asyncio.run(main())
