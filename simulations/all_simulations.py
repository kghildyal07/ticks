import time
import random
import asyncio
import requests
from threading import Thread


from const import TICK_URL, STATS_URL, INSTRUMENTS


# Global dictionary to store statistics for each instrument
statistics_results = {
    "all": [],
    "per_instrument": {instrument: [] for instrument in INSTRUMENTS},
}


def generate_tick(instrument: str):
    """
    Function to generate a tick with the correct timestamp (current time)
    """
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    price = round(random.uniform(100, 1500), 2)  # Random price between 100 and 1500
    return {"instrument": instrument, "price": price, "timestamp": timestamp}


def generate_outdated_tick(instrument: str):
    """
    Function to simulate the addition of outdated ticks (older than 60 seconds)
    """
    timestamp = int(
        (time.time() - 70) * 1000
    )  # Simulate a timestamp that is 70 seconds old
    price = round(random.uniform(100, 1500), 2)
    return {"instrument": instrument, "price": price, "timestamp": timestamp}


async def post_tick(tick: dict):
    """
    Function to simulate sending a POST request to /ticks to add a tick

    """
    response = requests.post(f"{TICK_URL}/", json=tick)
    if response.status_code == 201:
        print(f"Tick {tick['instrument']} added successfully")
    elif response.status_code == 204:
        print(f"Failed to add tick {tick['instrument']} - older than 60 seconds")
    else:
        print(f"Failed to add tick {tick['instrument']}")


def get_statistics():
    """
    Function to call the /statistics API to get global statistics
    """
    response = requests.get(f"{STATS_URL}/")
    if response.status_code == 200:
        stats = response.json()
        statistics_results["all"].append(stats)
        print("Global Statistics:", stats)
    else:
        print("Failed to fetch global statistics")


def get_instrument_statistics(instrument: str):
    """
    Function to call the /statistics/{instrument} API to get statistics for a specific instrument

    """
    response = requests.get(f"{STATS_URL}/{instrument}")
    if response.status_code == 200:
        stats = response.json()
        statistics_results["per_instrument"][instrument].append(stats)
        print(f"{instrument} Statistics:", stats)
    else:
        print(f"Failed to fetch statistics for {instrument}")


async def simulate_ticks(rounds):
    """
    Function to simulate the cache population and API calls
    """
    cont = 0
    while cont < rounds:
        # Randomly choose an instrument
        instrument = random.choice(INSTRUMENTS)

        # Generate a tick with the correct timestamp and post it
        tick = generate_tick(instrument)
        await post_tick(tick)

        # Simulate sending an outdated tick (older than 60 seconds) and post it
        outdated_tick = generate_outdated_tick(instrument)
        await post_tick(outdated_tick)

        # Random delay between tick simulations
        await asyncio.sleep(random.uniform(0.5, 1.5))
        cont += 1


async def fetch_statistics_periodically(rounds):
    """
    Function to periodically fetch and print statistics

    """
    cont = 0
    while cont < rounds:
        # Fetch global statistics
        get_statistics()

        # Fetch statistics for each instrument
        for instrument in INSTRUMENTS:
            get_instrument_statistics(instrument)

        # Wait before fetching again
        await asyncio.sleep(5)
        cont += 1


def run_simulation():
    """
    Main function to run the simulation in parallel
    """
    # Manually set the event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Simulate ticks and periodically fetch statistics
    rounds = 10
    tasks = [
        loop.create_task(simulate_ticks(rounds)),
        loop.create_task(fetch_statistics_periodically(rounds)),
    ]

    loop.run_until_complete(asyncio.gather(*tasks))


# Run the simulation
if __name__ == "__main__":
    # Run the simulation in a separate thread to avoid blocking the main thread
    simulation_thread = Thread(target=run_simulation)
    simulation_thread.start()
