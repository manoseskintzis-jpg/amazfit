import asyncio
from bleak import BleakClient

ADDRESS = "C8:55:3B:6C:97:7D"
FW_UUID = "00002a28-0000-1000-8000-00805f9b34fb"  # Firmware Version
HW_UUID = "00002a27-0000-1000-8000-00805f9b34fb"  # Hardware Version
SN_UUID = "00002a25-0000-1000-8000-00805f9b34fb"  # Serial Number

async def main():
    async with BleakClient(ADDRESS) as client:
        fw_raw = await client.read_gatt_char(FW_UUID)
        hw_raw = await client.read_gatt_char(HW_UUID)
        sn_raw = await client.read_gatt_char(SN_UUID)
        
        fw = fw_raw.decode('utf-8', errors='ignore').strip('\x00')
        hw = hw_raw.decode('utf-8', errors='ignore').strip('\x00')
        sn = sn_raw.decode('utf-8', errors='ignore').strip('\x00')
        
        print(f"--- Amazfit GTR Info ---")
        print(f"MAC Address: {ADDRESS}")
        print(f"Firmware:    {fw}")
        print(f"Hardware:    {hw}")
        print(f"Serial No:   {sn}")

asyncio.run(main())
