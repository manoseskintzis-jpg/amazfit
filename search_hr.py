import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Scanning all readable characteristics with a timeout...")
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        val = await asyncio.wait_for(
                            client.read_gatt_char(char.uuid), timeout=1.0
                        )
                        if 76 in val:
                            print(f"[FOUND] UUID: {char.uuid} at index {list(val).index(76)}")
                            print(f"  Data: {list(val)}")
                    except Exception:
                        # Skip characteristics that timeout or reject reads
                        pass
        print("Scan complete.")

asyncio.run(main())
