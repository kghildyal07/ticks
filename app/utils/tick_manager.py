import time
import asyncio
from typing import Dict
from collections import deque
from app.utils.helper import calculate_stats


class TickManager:
    """
    The main class of the service that stores the ticks in 2 cachce
    It is also resonsible for maintaing the cache with the latests data
    """

    def __init__(self):
        self.all_ticks = deque()
        self.instrument_ticks: Dict[str, deque] = {}
        self.lock = asyncio.Lock()

    async def add(self, tick: dict) -> bool:
        """
        To add ticks to the deque cache
        """
        async with self.lock:
            current_timestamp = int(time.time() * 1000)

            if tick.timestamp < current_timestamp - 60000:
                return False  # Tick is older than 60 seconds, ignore it

            # Add tick to all list
            self.all_ticks.append(tick.model_dump())
            self.remove(self.all_ticks, current_timestamp)

            # Add tick to instrument-specific list
            if tick.instrument not in self.instrument_ticks:
                self.instrument_ticks[tick.instrument] = deque()
            self.instrument_ticks[tick.instrument].append(tick.model_dump())
            self.remove(self.instrument_ticks[tick.instrument], current_timestamp)

            return True  # Successfully added the tick

    def remove(self, ticks: dict, current_timestamp: int):
        """
        To remove the ticks older than 60 seconds
        """
        while ticks and ticks[0]["timestamp"] <= current_timestamp - 60000:
            ticks.popleft()

    def clear(self):
        """
        To clear the cache when app shuts down
        """
        self.all_ticks.clear()
        self.instrument_ticks.clear()

    async def get_all_stats(self) -> dict:
        """
        Function to calculate the stats for all the instruments
        """
        async with self.lock:
            current_timestamp = int(time.time() * 1000)
            self.remove(self.all_ticks, current_timestamp)
            return calculate_stats(self.all_ticks)

    async def get_instrument_stats(self, ticker: str):
        """
        Function to calculate the stats for the requests instrument
        """
        async with self.lock:
            current_timestamp = int(time.time() * 1000)
            if ticker not in self.instrument_ticks:
                return {"avg": 0.0, "max": 0.0, "min": 0.0, "count": 0}
            self.remove(self.instrument_ticks[ticker], current_timestamp)
            return calculate_stats(self.instrument_ticks[ticker])
