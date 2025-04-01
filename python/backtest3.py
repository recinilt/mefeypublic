import requests
import time
from datetime import datetime
import csv
import os
import sys

# Binance API URL
BINANCE_API_BASE = "https://api.binance.com/api/v3/"

def fetch_klines(symbol, interval, limit):
    url = f"{BINANCE_API_BASE}klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return []

def save_to_file(data, filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

def calculate_ema(prices, period):
    ema = []
    multiplier = 2 / (period + 1)
    for i in range(len(prices)):
        if i < period - 1:
            ema.append(None)  # Not enough data to calculate EMA
        elif i == period - 1:
            ema.append(sum(prices[:period]) / period)  # SMA for the first EMA
        else:
            ema.append((prices[i] - ema[-1]) * multiplier + ema[-1])
    return ema

def progress_bar(current, total, bar_length=30):
    fraction = current / total
    arrow = "=" * int(fraction * bar_length - 1) + ">"
    padding = " " * (bar_length - len(arrow))
    end = '\r' if current < total else '\n'
    print(f"[{arrow}{padding}] {int(fraction * 100)}%", end=end)
    sys.stdout.flush()

def analyze_trades(btc_data, eth_data):
    best_results = []

    total_combinations = ((21 - 5) * (51 - 20)) * 21
    combination_count = 0

    for short_ema_period in range(5, 21):
        for long_ema_period in range(20, 51):
            if short_ema_period >= long_ema_period:
                continue

            for order_ratio_threshold in [x / 10 for x in range(10, 31)]:
                combination_count += 1
                progress_bar(combination_count, total_combinations)

                btc_prices = [float(row[4]) for row in btc_data]  # Close prices
                btc_ema_short = calculate_ema(btc_prices, short_ema_period)
                btc_ema_long = calculate_ema(btc_prices, long_ema_period)

                balance = 1000  # Start with $1000
                btc_holding = 0
                trades = []

                for i in range(len(btc_prices)):
                    if i < max(short_ema_period, long_ema_period):
                        continue

                    ema_short = btc_ema_short[i]
                    ema_long = btc_ema_long[i]

                    if ema_short is None or ema_long is None:
                        continue

                    buy_orders = sum(float(row[1]) for row in btc_data[i-1440:i] if float(row[4]) <= btc_prices[i] * 0.97)
                    sell_orders = sum(float(row[1]) for row in btc_data[i-1440:i] if float(row[4]) >= btc_prices[i] * 1.03)

                    if sell_orders == 0:
                        continue

                    order_ratio = buy_orders / sell_orders

                    if order_ratio > order_ratio_threshold and ema_short > ema_long:
                        # Buy signal
                        if balance > 0:
                            btc_holding = balance / btc_prices[i]
                            balance = 0
                            trades.append(("BUY", btc_prices[i]))
                    elif btc_holding > 0 and (ema_short <= ema_long or order_ratio <= order_ratio_threshold):
                        # Sell signal
                        balance = btc_holding * btc_prices[i]
                        btc_holding = 0
                        trades.append(("SELL", btc_prices[i]))

                final_balance = balance + (btc_holding * btc_prices[-1])
                trade_count = len(trades)

                if trade_count > 0:
                    best_results.append((final_balance, trade_count, short_ema_period, long_ema_period, order_ratio_threshold))

    # Sort by balance and return the top 50
    best_results.sort(reverse=True, key=lambda x: x[0])
    return best_results[:50]

# Fetch data
print("Fetching BTCUSDT data...")
btc_data = fetch_klines("BTCUSDT", "1m", 1440)
print("Fetching ETHUSDT data...")
eth_data = fetch_klines("ETHUSDT", "1m", 1440)

if btc_data and eth_data:
    # Save data to timestamped files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    btc_filename = f"BTCUSDT_{timestamp}.csv"
    eth_filename = f"ETHUSDT_{timestamp}.csv"

    save_to_file(btc_data, btc_filename)
    save_to_file(eth_data, eth_filename)

    # Analyze trades
    print("Analyzing trades...")
    results = analyze_trades(btc_data, eth_data)

    # Print results
    print("\nTop 50 Results:")
    for result in results:
        print(f"Balance: {result[0]:.2f}, Trades: {result[1]}, Short EMA: {result[2]}, Long EMA: {result[3]}, Order Ratio Threshold: {result[4]:.2f}")
