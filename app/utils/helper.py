def calculate_stats(ticks: dict) -> dict:
    """
    Function to calculate statistics from a list of ticks
    """
    if not ticks:
        return {"avg": 0.0, "max": 0.0, "min": 0.0, "count": 0}

    prices = [tick["price"] for tick in ticks]
    return {
        "avg": sum(prices) / len(prices),
        "max": max(prices),
        "min": min(prices),
        "count": len(prices),
    }
