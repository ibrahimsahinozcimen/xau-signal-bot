import requests
import pandas as pd


def get_data():
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        "?period1=0&period2=9999999999"
        "&interval=15m"
        "&range=5d"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()["chart"]["result"][0]

    timestamps = data["timestamp"]
    quote = data["indicators"]["quote"][0]

    df = pd.DataFrame({
        "time": pd.to_datetime(timestamps, unit="s"),
        "open": quote["open"],
        "high": quote["high"],
        "low": quote["low"],
        "close": quote["close"],
        "volume": quote["volume"]
    })

    df = df.dropna()

    return df
