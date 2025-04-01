import numpy as np
from binance.client import Client
from binance.enums import *
from tqdm import tqdm

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"  # Futures trading pair
interval = "1m"  # 1-minute interval
vwap_offset = 0.0015
stop_loss_perc = 0.0013
quantity = 0.001  # Adjust based on balance and risk

# Function to calculate VWAP
def calculate_vwap(candles):
    prices = np.array([float(c[4]) for c in candles])  # Close prices
    volumes = np.array([float(c[5]) for c in candles])  # Volumes
    return np.sum(prices * volumes) / np.sum(volumes)

# Fetch historical data
candles = client.futures_klines(symbol=symbol, interval=interval, limit=1440)  # Fetch 1440 1-minute candles

# Optimization range
take_profit_range = np.linspace(0.003, 0.05, 100)
results = []

# Optimization loop
for take_profit_perc in tqdm(take_profit_range, desc="Optimizing"):
    # Backtest parameters
    starting_balance = 1000  # Initial balance in USDT
    balance = starting_balance
    commission_rate = 0.0004  # Binance commission rate per trade
    trades = []  # Store trade details
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

                # Check stop-loss or take-profit for long position
                if close_price <= position['stop_loss_price'] or close_price >= position['take_profit_price']:
                    profit = (position['take_profit_price'] if close_price >= position['take_profit_price'] else close_price) - position['entry_price']
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = (profit * quantity) - commission
                    balance += net_profit
                    trades.append({"type": "LONG", "entry": position['entry_price'], "exit": close_price, "profit": net_profit, "balance": balance})
                    has_open_position = False

            elif position['side'] == "SELL":
                position['stop_loss_price'] = vwap * (1 + stop_loss_perc)

                # Check stop-loss or take-profit for short position
                if close_price >= position['stop_loss_price'] or close_price <= position['take_profit_price']:
                    profit = position['entry_price'] - (position['take_profit_price'] if close_price <= position['take_profit_price'] else close_price)
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = (profit * quantity) - commission
                    balance += net_profit
                    trades.append({"type": "SHORT", "entry": position['entry_price'], "exit": close_price, "profit": net_profit, "balance": balance})
                    has_open_position = False

    # Store results if trades were made
    if trades:
        results.append({
            "take_profit": take_profit_perc,
            "final_balance": balance,
            "num_trades": len(trades)
        })

# Sort and display top results
sorted_results = sorted(results, key=lambda x: x["final_balance"], reverse=True)[:50]
print("\nTop 50 Optimized Results:")
for idx, result in enumerate(sorted_results):
    print(f"{idx+1}. TP: {result['take_profit']:.4f}, Final Balance: {result['final_balance']:.2f}, Trades: {result['num_trades']}")
