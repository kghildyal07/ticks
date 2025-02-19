#  FastAPI server URL
BASE = "http://127.0.0.1:8000/v1"
TICK_URL = f"{BASE}/ticks"
STATS_URL = f"{BASE}/statistics"


# List of instruments (can be expanded or replaced with real instruments)
INSTRUMENTS = [
    "AAPL",  # Apple Inc.
    "GOOG",  # Alphabet Inc. (Google)
    "TSLA",  # Tesla Inc.
    "IBM.N",  # IBM (New York Stock Exchange)
    "AMZN",  # Amazon.com, Inc.
    "MSFT",  # Microsoft Corporation
    "NVDA",  # NVIDIA Corporation
    "META",  # Meta Platforms (formerly Facebook)
    "NFLX",  # Netflix, Inc.
    "BA",  # Boeing Co.
]
