import time
import random
import aiohttp
import asyncio
from datetime import datetime

from const import TICK_URL, INSTRUMENTS


# Simulate generating a past tick older than 60 seconds
async def generate_past_tick():
    # Randomly pick an instrument
    instrument = random.choice(INSTRUMENTS)

    # Generate a random price between 100 and 200
    price = round(random.uniform(100, 200), 2)

    # Get the current timestamp (in milliseconds)
    current_timestamp = int(time.time() * 1000)

    # Simulate a past tick by subtracting more than 60 seconds (e.g., 120 seconds = 2 minutes)
    past_timestamp = current_timestamp - (120 * 1000)  # 2 minutes earlier

    # Return the tick data
    return {"instrument": instrument, "price": price, "timestamp": past_timestamp}


# Function to send the tick to the FastAPI server asynchronously
async def send_tick(session, tick):
    try:
        async with session.post(TICK_URL, json=tick) as response:
            if response.status == 201:
                print(f"[{datetime.now()}] Tick successfully added: {tick}")
            elif response.status == 204:
                print(
                    f"[{datetime.now()}] Tick ignored (older than 60 seconds): {tick}"
                )
            else:
                print(
                    f"[{datetime.now()}] Unexpected response: {response.status} - {await response.text()}"
                )
    except Exception as e:
        print(f"Error sending tick: {e}")


# Function to send multiple past ticks concurrently
async def send_past_ticks_concurrently(num_ticks=60):
    # Create an aiohttp session for making asynchronous requests
    async with aiohttp.ClientSession() as session:
        tasks = []

        # Generate and send past ticks concurrently
        for _ in range(num_ticks):
            tick = await generate_past_tick()
            task = asyncio.create_task(send_tick(session, tick))
            tasks.append(task)

        # Wait for all tasks to finish
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    num_ticks = 100  # Simulate sending 100 past ticks (can be adjusted)
    asyncio.run(send_past_ticks_concurrently(num_ticks))
