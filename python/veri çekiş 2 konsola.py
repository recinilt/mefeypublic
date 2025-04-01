import csv
import requests
from datetime import datetime, timedelta, timezone
from tqdm import tqdm

def fetch_binance_klines(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": int(start_time.timestamp() * 1000),
        "endTime": int(end_time.timestamp() * 1000),
        "limit": 1000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data from Binance: {response.status_code} {response.text}")

def collect_data(symbol, interval, days_back):
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)  # UTC-aware
    start_time = (end_time - timedelta(days=days_back)).replace(tzinfo=timezone.utc)  # UTC-aware

    print(f"Fetching data for {symbol} with interval {interval}...")
    all_data = []
    current_start_time = start_time

    total_steps = (end_time - start_time).days + 1
    with tqdm(total=total_steps, desc=f"Processing {symbol} - {interval}") as pbar:
        while current_start_time < end_time:
            current_end_time = min(current_start_time + timedelta(days=1), end_time)
            try:
                klines = fetch_binance_klines(symbol, interval, current_start_time, current_end_time)
                for kline in klines:
                    timestamp = datetime.fromtimestamp(kline[0] / 1000, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    open_price = kline[1]
                    high_price = kline[2]
                    low_price = kline[3]
                    close_price = kline[4]
                    volume = kline[5]
                    all_data.append([timestamp, open_price, high_price, low_price, close_price, volume])
                current_start_time = datetime.fromtimestamp(klines[-1][6] / 1000, tz=timezone.utc)
            except Exception as e:
                print(f"Error fetching data: {e}")
                break

            pbar.update(1)

    return all_data

if __name__ == "__main__":
    # Kullanıcıdan input alma
    symbol = input("Enter the coin pair (e.g., BTCUSDT): ").strip().upper()
    interval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))

    # Veri toplama
    data = collect_data(symbol, interval, days_back)

    # Sonuçları konsola yazdırma
    print("\nFetched Data:")
    for row in data:
        print(row)
