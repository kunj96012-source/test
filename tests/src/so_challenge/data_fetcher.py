import pandas as pd
import requests
import time
from datetime import datetime
from pathlib import Path


def fetch_data(cache_path="data.csv", retries=3):
    """
    Fetch Stack Overflow data, cache it locally, and return DataFrame.
    """

    cache_path = Path(cache_path)

    # ✅ 1. If cache exists → load it
    if cache_path.exists():
        return pd.read_csv(cache_path, parse_dates=["year_month"])

    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "site": "stackoverflow",
        "pagesize": 100
    }

    # ✅ 2. Retry logic
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)

            if response.status_code != 200:
                raise Exception("Bad response")

            data = response.json()["items"]

            break

        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(1)

    # ✅ 3. Convert to DataFrame
    dates = [
        datetime.utcfromtimestamp(item["creation_date"])
        for item in data
    ]

    df = pd.DataFrame({"date": dates})

    # Group by month
    df["year_month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df = df.groupby("year_month").size().reset_index(name="question_count")

    # ✅ 4. Save cache
    df.to_csv(cache_path, index=False)

    return df