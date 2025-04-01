import numpy as np
from tqdm import tqdm
from binance.client import Client
from binance.enums import *
from itertools import product

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"  # Futures trading pair
interval = "1m"  # 1-minute interval
quantity = 0.001  # Adjust based on balance and risk
starting_balance = 1000  # Initial balance in USDT
commission_rate = 0.0004  # Binance commission rate per trade

# Function to calculate VWAP
def calculate_vwap(candles):
    prices = np.array([float(c[4]) for c in candles])  # Close prices
    volumes = np.array([float(c[5]) for c in candles])  # Volumes
    return np.sum(prices * volumes) / np.sum(volumes)

# Fetch historical data
candles = client.futures_klines(symbol=symbol, interval=interval, limit=1440)  # Fetch 1440 1-minute candles

# Define parameter ranges
vwap_offsets = np.linspace(0.0005, 0.01, 10)
take_profit_percs = np.linspace(0.003, 0.1, 10)
stop_loss_percs = np.linspace(0.0005, 0.05, 10)

# Storage for results
results = []

# Backtest loop over parameter combinations
param_combinations = list(product(vwap_offsets, take_profit_percs, stop_loss_percs))

print("Starting backtest...")
for vwap_offset, take_profit_perc, stop_loss_perc in tqdm(param_combinations):
    balance = starting_balance
    trades = []
    has_open_position = False
    position = {
        'side': None,
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
            # Update stop-loss dynamically based on VWAP
            if position['side'] == "BUY":
                position['stop_loss_price'] = vwap * (1 - stop_loss_perc)

                # Check stop-loss or take-profit for long position
                if close_price <= position['stop_loss_price'] or close_price >= position['take_profit_price']:
                    profit = (close_price - position['entry_price']) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({"type": "LONG", "entry": position['entry_price'], "exit": close_price, "profit": net_profit})
                    has_open_position = False

            elif position['side'] == "SELL":
                position['stop_loss_price'] = vwap * (1 + stop_loss_perc)

                # Check stop-loss or take-profit for short position
                if close_price >= position['stop_loss_price'] or close_price <= position['take_profit_price']:
                    profit = (position['entry_price'] - close_price) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({"type": "SHORT", "entry": position['entry_price'], "exit": close_price, "profit": net_profit})
                    has_open_position = False

    if trades:
        results.append({
            "vwap_offset": vwap_offset,
            "take_profit_perc": take_profit_perc,
            "stop_loss_perc": stop_loss_perc,
            "final_balance": balance,
            "total_trades": len(trades)
        })

# Sort results by final balance in descending order
results = sorted(results, key=lambda x: x["final_balance"], reverse=True)

# Display top 50 results
print("\nTop 50 Results:")
print("{:<15} {:<20} {:<20} {:<15} {:<15}".format("VWAP Offset", "Take Profit %", "Stop Loss %", "Trades", "Final Balance"))
for result in results[:400]:
    print("{:<15.4f} {:<20.4f} {:<20.4f} {:<15} {:<15.2f}".format(
        result["vwap_offset"],
        result["take_profit_perc"],
        result["stop_loss_perc"],
        result["total_trades"],
        result["final_balance"]
    ))
