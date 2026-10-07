import asyncio
from bleak import BleakClient
import struct
import json
from datetime import datetime
from pathlib import Path

ADDRESS = "C8:55:3B:6C:97:7D"
BATTERY_CHAR_UUID = "00000006-0000-3512-2118-0009af100700"
STEPS_CHAR_UUID = "00000007-0000-3512-2118-0009af100700"

async def main():
    async with BleakClient(ADDRESS) as client:
        # 1. Read Battery
        bat_val = await client.read_gatt_char(BATTERY_CHAR_UUID)
        battery_level = bat_val[1]
        is_charging = bat_val[2] == 1
        
        # 2. Read Activity Telemetry
        act_val = await client.read_gatt_char(STEPS_CHAR_UUID)
        steps = struct.unpack_from('<H', act_val, 1)[0]
        distance_m = struct.unpack_from('<H', act_val, 5)[0]
        calories = struct.unpack_from('<H', act_val, 9)[0] if len(act_val) >= 11 else 0
        
        # 3. Upsert into JSON Database by Date
        history_file = Path(__file__).parent / "history.json"
        
        history_data = []
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history_data = json.load(f)
            except json.JSONDecodeError:
                history_data = []
                
        now = datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        timestamp_full = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if today's entry already exists
        updated = False
        for entry in history_data:
            # If entry is keyed by date or contains date prefix
            entry_date = entry.get("timestamp", "").split(" ")[0]
            if entry_date == today_date:
                # Update with latest values for today
                entry["timestamp"] = timestamp_full
                entry["battery"] = battery_level
                entry["charging"] = is_charging
                entry["steps"] = steps
                entry["distance_m"] = distance_m
                entry["calories"] = calories
                updated = True
                break
                
        # If today doesn't exist yet, append a new record
        if not updated:
            history_data.append({
                "timestamp": timestamp_full,
                "battery": battery_level,
                "charging": is_charging,
                "steps": steps,
                "distance_m": distance_m,
                "calories": calories
            })
            
        # Sort history chronologically by date to keep things neat
        history_data.sort(key=lambda x: x["timestamp"])

        with open(history_file, "w") as f:
            json.dump(history_data, f, indent=4)

        print(f"--- Amazfit GTR Status ---")
        print(f"Battery:    {battery_level}% (Charging: {is_charging})")
        print(f"Steps:      {steps}")
        print(f"Distance:   {distance_m} meters")
        print(f"Calories:   {calories} kcal")
        print(f"[Database updated for {today_date}]")

asyncio.run(main())
