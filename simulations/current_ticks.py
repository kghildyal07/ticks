import time
import random
import aiohttp
import asyncio
from datetime import datetime

from const import TICK_URL, INSTRUMENTS


async def generate_tick() -> dict:
    """
    Simulate sending ticks asynchronously
    """

    # Randomly pick an instrument
    instrument = random.choice(INSTRUMENTS)

    # Generate a random price between 100 and 200
    price = round(random.uniform(100, 200), 2)

    # Get the current timestamp (in milliseconds)
    timestamp = int(time.time() * 1000)

    # Return the tick data
    return {"instrument": instrument, "price": price, "timestamp": timestamp}


async def send_tick(session, tick):
    """
    Function to send the tick to the FastAPI server asynchronously
    """
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


async def send_ticks_concurrently(num_ticks=60):
    """
    Function to send multiple ticks concurrently
    """
    # Create an aiohttp session for making asynchronous requests
    async with aiohttp.ClientSession() as session:
        tasks = []

        # Generate and send ticks concurrently
        for _ in range(num_ticks):
            tick = await generate_tick()
            task = asyncio.create_task(send_tick(session, tick))
            tasks.append(task)

        # Wait for all tasks to finish
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    num_ticks = 10000  # Simulate sending 10000 ticks (adjust the number as needed)
    asyncio.run(send_ticks_concurrently(num_ticks))
