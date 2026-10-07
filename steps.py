import asyncio
from bleak import BleakClient
import struct

ADDRESS = "C8:55:3B:6C:97:7D"
STEPS_CHAR_UUID = "00000007-0000-3512-2118-0009af100700"

async def main():
    async with BleakClient(ADDRESS) as client:
        val = await client.read_gatt_char(STEPS_CHAR_UUID)
        print(f"Raw Hex: {val.hex()}")
        
        # Test common little-endian integer offsets for step data
        if len(val) >= 4:
            print(f"UInt32 at offset 0: {struct.unpack_from('<I', val, 0)[0]}")
        if len(val) >= 6:
            print(f"UInt16 at offset 1: {struct.unpack_from('<H', val, 1)[0]}")
            print(f"UInt32 at offset 2: {struct.unpack_from('<I', val, 2)[0]}")
        if len(val) >= 8:
            print(f"UInt32 at offset 4: {struct.unpack_from('<I', val, 4)[0]}")

asyncio.run(main())
