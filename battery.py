import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"
# Characteristic 06 handles battery info and charging status on Huami devices
BATTERY_CHAR_UUID = "00000006-0000-3512-2118-0009af100700"

async def main():
    async with BleakClient(ADDRESS) as client:
        val = await client.read_gatt_char(BATTERY_CHAR_UUID)
        print(f"Raw Hex: {val.hex()}")
        
        # val[1] is the battery percentage, val[2] is charging state (1 = charging, 0 = not)
        battery_level = val[1]
        is_charging = val[2] == 1
        
        print(f"Battery Level: {battery_level}%")
        print(f"Charging: {is_charging}")

asyncio.run(main())
