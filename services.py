import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"

async def main():
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        for service in client.services:
            print(f"[Service] {service.uuid} - {service.description}")
            for char in service.characteristics:
                print(f"  [Char] {char.uuid} ({','.join(char.properties)})")

asyncio.run(main())
