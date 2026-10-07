import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected. Scanning readable characteristics...\n")
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        val = await client.read_gatt_char(char.uuid)
                        print(f"UUID: {char.uuid}\n  Value (Hex): {val.hex()}\n  Decimals: {list(val)}\n")
                    except Exception:
                        pass

asyncio.run(main())
