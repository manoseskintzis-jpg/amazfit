import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"
STEPS_CHAR_UUID = "00000007-0000-3512-2118-0009af100700"

async def main():
    async with BleakClient(ADDRESS) as client:
        val = await client.read_gatt_char(STEPS_CHAR_UUID)
        print(f"Full Hex: {val.hex()}")
        for i, b in enumerate(val):
            print(f"Index {i}: {b} (hex: {hex(b)})")

asyncio.run(main())
