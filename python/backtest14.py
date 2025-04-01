import numpy as np
from binance.client import Client
from binance.enums import *
from tqdm import tqdm  # For progress bar

# Binance API credentials (Dummy keys for example purposes)
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"  # Futures trading pair
interval = "1m"  # 1-minute interval
vwap_offset = 0.0015
take_profit_perc = 0.0120
quantity = 0.001  # Adjust based on balance and risk

# Function to calculate VWAP
def calculate_vwap(candles):
    prices = np.array([float(c[4]) for c in candles])  # Close prices
    volumes = np.array([float(c[5]) for c in candles])  # Volumes
    return np.sum(prices * volumes) / np.sum(volumes)

# Fetch historical data
candles = client.futures_klines(symbol=symbol, interval=interval, limit=1440)  # Fetch 1440 1-minute candles

# Backtest function
def backtest(stop_loss_perc):
    starting_balance = 1000  # Initial balance in USDT
    balance = starting_balance
    commission_rate = 0.0004  # Binance commission rate per trade
    trades = []

    has_open_position = False
    position = {
        'side': None,  # "BUY" or "SELL"
        'entry_price': None,
        'stop_loss_price': None,
        'take_profit_price': None
    }

    for i in range(20, len(candles)):
        window = candles[i-20:i]  # 20-candle window for VWAP calculation
        vwap = calculate_vwap(window)
        close_price = float(candles[i][4])

        # Calculate entry levels
        long_entry_level = vwap * (1 + vwap_offset)
        short_entry_level = vwap * (1 - vwap_offset)

        if not has_open_position:
            # Long condition
            if close_price > long_entry_level:
                position['side'] = "BUY"
                position['entry_price'] = close_price
                position['stop_loss_price'] = vwap * (1 - stop_loss_perc)
                position['take_profit_price'] = close_price * (1 + take_profit_perc)
                has_open_position = True

            # Short condition
            elif close_price < short_entry_level:
                position['side'] = "SELL"
                position['entry_price'] = close_price
                position['stop_loss_price'] = vwap * (1 + stop_loss_perc)
                position['take_profit_price'] = close_price * (1 - take_profit_perc)
                has_open_position = True

        else:
            if position['side'] == "BUY":
                position['stop_loss_price'] = vwap * (1 - stop_loss_perc)

                if close_price <= position['stop_loss_price']:
                    profit = (close_price - position['entry_price']) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append(net_profit)
                    has_open_position = False

                elif close_price >= position['take_profit_price']:
                    profit = (position['take_profit_price'] - position['entry_price']) * quantity
                    commission = (position['entry_price'] + position['take_profit_price']) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append(net_profit)
                    has_open_position = False

            elif position['side'] == "SELL":
                position['stop_loss_price'] = vwap * (1 + stop_loss_perc)

                if close_price >= position['stop_loss_price']:
                    profit = (position['entry_price'] - close_price) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append(net_profit)
                    has_open_position = False

                elif close_price <= position['take_profit_price']:
                    profit = (position['entry_price'] - position['take_profit_price']) * quantity
                    commission = (position['entry_price'] + position['take_profit_price']) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append(net_profit)
                    has_open_position = False

    return balance, len(trades)

# Parameter optimization
results = []
stop_loss_range = np.linspace(0.0005, 0.01, 100)  # Generate 100 values between 0.0005 and 0.01

for stop_loss_perc in tqdm(stop_loss_range, desc="Optimizing Stop Loss"):
    final_balance, trade_count = backtest(stop_loss_perc)
    if trade_count > 0:  # Only consider configurations with trades
        results.append((stop_loss_perc, final_balance, trade_count))

# Sort and display results
results = sorted(results, key=lambda x: x[1], reverse=True)  # Sort by final balance

print("Top 50 Configurations:")
print(f"{'Stop Loss':<10} {'Final Balance':<15} {'Trade Count':<12}")
print("-" * 40)
for stop_loss_perc, final_balance, trade_count in results[:50]:
    print(f"{stop_loss_perc:<10.5f} {final_balance:<15.2f} {trade_count:<12}")
