import pandas as pd
import numpy as np
from binance.client import Client

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
period = 1440  # 1440 minutes = 1 day
initial_balance = 1000  # Initial balance in USD
trade_quantity = 0.005  # Quantity to trade in BTC

# Strategy parameters
vwap_offset = 0.0016  # Entry offset from VWAP
take_profit_perc = 0.0138
stop_loss_perc = 0.006

# Fetch historical data
def fetch_historical_data(symbol, interval, period):
    candles = client.futures_klines(symbol=symbol, interval=interval, limit=period)
    df = pd.DataFrame(candles, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df[["timestamp", "close", "volume"]]

# Calculate VWAP
def calculate_vwap(df):
    cumulative_price_volume = (df["close"] * df["volume"]).cumsum()
    cumulative_volume = df["volume"].cumsum()
    df["vwap"] = cumulative_price_volume / cumulative_volume
    return df

# Backtest logic
def backtest(data, initial_balance, trade_quantity):
    balance = initial_balance
    position = None
    entry_price = 0
    trades = 0

    for index, row in data.iterrows():
        close_price = row["close"]
        vwap = row["vwap"]

        long_entry = vwap * (1 + vwap_offset)
        short_entry = vwap * (1 - vwap_offset)

        if position is None:
            # Entry conditions
            if close_price > long_entry:
                position = "LONG"
                entry_price = close_price
                trades += 1
            elif close_price < short_entry:
                position = "SHORT"
                entry_price = close_price
                trades += 1

        else:
            # Exit conditions
            if position == "LONG":
                take_profit = entry_price * (1 + take_profit_perc)
                stop_loss = entry_price * (1 - stop_loss_perc)
                if close_price >= take_profit or close_price <= stop_loss:
                    balance += (close_price - entry_price) * trade_quantity
                    position = None

            elif position == "SHORT":
                take_profit = entry_price * (1 - take_profit_perc)
                stop_loss = entry_price * (1 + stop_loss_perc)
                if close_price <= take_profit or close_price >= stop_loss:
                    balance += (entry_price - close_price) * trade_quantity
                    position = None

    return trades, balance

# Main execution
if __name__ == "__main__":
    print("Fetching historical data...")
    historical_data = fetch_historical_data(symbol, interval, period)
    historical_data = calculate_vwap(historical_data)

    print("Running backtest...")
    trades, final_balance = backtest(historical_data, initial_balance, trade_quantity)

    print(f"Total trades: {trades}")
    print(f"Final balance: ${final_balance:.2f}")
