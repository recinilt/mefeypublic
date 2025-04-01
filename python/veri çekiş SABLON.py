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

def save_to_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for row in data:
            writer.writerow(row)

def collect_data(symbols, intervals, days_back):
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)  # UTC-aware
    start_time = (end_time - timedelta(days=days_back)).replace(tzinfo=timezone.utc)  # UTC-aware

    for symbol in symbols:
        for interval in intervals:
            print(f"Fetching data for {symbol} at interval {interval}...")
            all_data = []
            current_start_time = start_time

            # Initialize progress bar
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
                        print(f"Error fetching data for {symbol} at interval {interval}: {e}")
                        break

                    # Update progress bar
                    pbar.update(1)

            filename = f"{symbol}_{interval}.csv"
            save_to_csv(filename, all_data)
            print(f"Data for {symbol} at interval {interval} saved to {filename}")

if __name__ == "__main__":
    symbols = ["BTCUSDT"]  # List of symbols
    intervals = ["1m"]  # List of intervals
    days_back = 365 # Fetch last 7 days of data
    collect_data(symbols, intervals, days_back)
