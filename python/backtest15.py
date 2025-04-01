import numpy as np
from binance.client import Client
from tqdm import tqdm

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"  # Futures trading pair
interval = "1m"  # 1-minute interval
take_profit_perc = 0.0120
stop_loss_perc = 0.0013
quantity = 0.001  # Adjust based on balance and risk

# Function to calculate VWAP
def calculate_vwap(candles):
    prices = np.array([float(c[4]) for c in candles])  # Close prices
    volumes = np.array([float(c[5]) for c in candles])  # Volumes
    return np.sum(prices * volumes) / np.sum(volumes)

# Fetch historical data
candles = client.futures_klines(symbol=symbol, interval=interval, limit=1440)  # Fetch 1440 1-minute candles

# VWAP offset range to test
vwap_offsets = np.linspace(0.0005, 0.01, 100)

# Backtest function
def backtest(vwap_offset):
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
            # Update stop-loss dynamically based on VWAP
            if position['side'] == "BUY":
                position['stop_loss_price'] = vwap * (1 - stop_loss_perc)

                # Check stop-loss or take-profit for long position
                if close_price <= position['stop_loss_price']:
                    profit = (close_price - position['entry_price']) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({
                        "type": "LONG",
                        "entry": position['entry_price'],
                        "exit": close_price,
                        "profit": net_profit,
                        "balance": balance
                    })
                    has_open_position = False

                elif close_price >= position['take_profit_price']:
                    profit = (position['take_profit_price'] - position['entry_price']) * quantity
                    commission = (position['entry_price'] + position['take_profit_price']) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({
                        "type": "LONG",
                        "entry": position['entry_price'],
                        "exit": position['take_profit_price'],
                        "profit": net_profit,
                        "balance": balance
                    })
                    has_open_position = False

            elif position['side'] == "SELL":
                position['stop_loss_price'] = vwap * (1 + stop_loss_perc)

                # Check stop-loss or take-profit for short position
                if close_price >= position['stop_loss_price']:
                    profit = (position['entry_price'] - close_price) * quantity
                    commission = (position['entry_price'] + close_price) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({
                        "type": "SHORT",
                        "entry": position['entry_price'],
                        "exit": close_price,
                        "profit": net_profit,
                        "balance": balance
                    })
                    has_open_position = False

                elif close_price <= position['take_profit_price']:
                    profit = (position['entry_price'] - position['take_profit_price']) * quantity
                    commission = (position['entry_price'] + position['take_profit_price']) * quantity * commission_rate
                    net_profit = profit - commission
                    balance += net_profit
                    trades.append({
                        "type": "SHORT",
                        "entry": position['entry_price'],
                        "exit": position['take_profit_price'],
                        "profit": net_profit,
                        "balance": balance
                    })
                    has_open_position = False

    return balance, len(trades)

# Optimization loop
results = []
for offset in tqdm(vwap_offsets, desc="Optimizing VWAP Offset"):
    final_balance, total_trades = backtest(offset)
    if total_trades > 0:
        results.append({
            "vwap_offset": offset,
            "final_balance": final_balance,
            "total_trades": total_trades
        })

# Sort results by final balance
sorted_results = sorted(results, key=lambda x: x['final_balance'], reverse=True)

# Display top 50 results
print("Top 50 Results:")
print("VWAP Offset | Final Balance | Total Trades")
for result in sorted_results[:50]:
    print(f"{result['vwap_offset']:.5f} | {result['final_balance']:.2f} | {result['total_trades']}")
