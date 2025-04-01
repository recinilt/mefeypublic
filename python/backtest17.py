import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
vwap_offset = 0.0016
take_profit_perc = 0.0138
stop_loss_perc = 0.006
quantity = 0.005

# Fetch historical data
def fetch_historical_data():
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=1440)

    klines = client.get_historical_klines(symbol, interval, start_time.strftime("%d %b %Y %H:%M:%S"),
                                          end_time.strftime("%d %b %Y %H:%M:%S"))
    df = pd.DataFrame(klines, columns=["time", "open", "high", "low", "close", "volume", "close_time", "qav", "num_trades", "taker_base", "taker_quote", "ignore"])
    df = df[["time", "open", "high", "low", "close", "volume"]]
    df["time"] = pd.to_datetime(df["time"], unit='ms')
    df.set_index("time", inplace=True)
    df = df.astype(float)
    return df

# Calculate VWAP
def calculate_vwap(df):
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

# Backtest strategy
def backtest(df):
    balance = 1000  # Initial balance in USDT
    trades = []
    calculate_vwap(df)

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i - 1]

        long_entry = row["close"] > prev_row["vwap"] * (1 + vwap_offset)
        short_entry = row["close"] < prev_row["vwap"] * (1 - vwap_offset)

        if long_entry:
            entry_price = row["close"]
            take_profit_price = entry_price * (1 + take_profit_perc)
            stop_loss_price = entry_price * (1 - stop_loss_perc)

            # Simulate long position
            for j in range(i + 1, len(df)):
                future_row = df.iloc[j]
                if future_row["close"] >= take_profit_price:
                    trades.append({"type": "LONG", "entry": entry_price, "exit": take_profit_price, "profit": take_profit_price - entry_price})
                    balance += (take_profit_price - entry_price) * quantity
                    break
                elif future_row["close"] <= stop_loss_price:
                    trades.append({"type": "LONG", "entry": entry_price, "exit": stop_loss_price, "profit": stop_loss_price - entry_price})
                    balance += (stop_loss_price - entry_price) * quantity
                    break

        elif short_entry:
            entry_price = row["close"]
            take_profit_price = entry_price * (1 - take_profit_perc)
            stop_loss_price = entry_price * (1 + stop_loss_perc)

            # Simulate short position
            for j in range(i + 1, len(df)):
                future_row = df.iloc[j]
                if future_row["close"] <= take_profit_price:
                    trades.append({"type": "SHORT", "entry": entry_price, "exit": take_profit_price, "profit": entry_price - take_profit_price})
                    balance += (entry_price - take_profit_price) * quantity
                    break
                elif future_row["close"] >= stop_loss_price:
                    trades.append({"type": "SHORT", "entry": entry_price, "exit": stop_loss_price, "profit": entry_price - stop_loss_price})
                    balance += (entry_price - stop_loss_price) * quantity
                    break

    return balance, trades

# Main
if __name__ == "__main__":
    df = fetch_historical_data()
    final_balance, trades = backtest(df)

    print("Backtest Results:")
    print(f"Initial Balance: $1000")
    print(f"Final Balance: ${final_balance:.2f}")
    print(f"Total Trades: {len(trades)}")
    print("Trade Details:")
    #for trade in trades:
        #print(trade)
