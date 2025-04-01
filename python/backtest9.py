import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
import matplotlib
matplotlib.use('Agg')  # Alternatif backend kullanımı


# Binance API credentials (bu API anahtarları sadece örnek amaçlıdır, çalışmayacaktır)
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"
interval = "1m"
lookback = 1440  # Number of periods for backtest
vwap_offset = 0.0015
take_profit_perc = 0.0050
stop_loss_perc = 0.0015
initial_balance = 1000  # USD
quantity = 0.001  # BTC

# Fetch historical data
candles = client.futures_klines(symbol=symbol, interval=interval, limit=lookback)
data = pd.DataFrame(candles, columns=[
    "timestamp", "open", "high", "low", "close", "volume", "close_time",
    "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
])
data = data[["timestamp", "close", "volume"]]
data["close"] = data["close"].astype(float)
data["volume"] = data["volume"].astype(float)
data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")

# Calculate VWAP
data["vwap"] = (data["close"] * data["volume"]).cumsum() / data["volume"].cumsum()
data["long_entry"] = data["vwap"] * (1 + vwap_offset)
data["short_entry"] = data["vwap"] * (1 - vwap_offset)

# Simulate backtest
balance = initial_balance
position = None
entry_price = 0
b_balance = [initial_balance]
timestamps = [data.loc[0, "timestamp"]]

for i in range(1, len(data)):
    close_price = data.loc[i, "close"]
    long_entry = data.loc[i, "long_entry"]
    short_entry = data.loc[i, "short_entry"]

    if position is None:
        if close_price > long_entry:
            position = "long"
            entry_price = close_price
            take_profit = entry_price * (1 + take_profit_perc)
            stop_loss = entry_price * (1 - stop_loss_perc)
        elif close_price < short_entry:
            position = "short"
            entry_price = close_price
            take_profit = entry_price * (1 - take_profit_perc)
            stop_loss = entry_price * (1 + stop_loss_perc)
    else:
        if position == "long":
            if close_price >= take_profit or close_price <= stop_loss:
                pnl = (close_price - entry_price) * quantity
                balance += pnl
                position = None
        elif position == "short":
            if close_price <= take_profit or close_price >= stop_loss:
                pnl = (entry_price - close_price) * quantity
                balance += pnl
                position = None

    b_balance.append(balance)
    timestamps.append(data.loc[i, "timestamp"])

# Grafik çizimi
assert len(b_balance) == len(timestamps), "b_balance ve timestamps aynı uzunlukta olmalı!"

plt.figure(figsize=(12, 6))
plt.plot(timestamps, b_balance, label="Balance", marker="o")
plt.title("Backtest Balance Over Time")
plt.xlabel("Time")
plt.ylabel("Balance (USD)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

plt.savefig("backtest_result.png")  # Grafiği PNG dosyası olarak kaydeder

