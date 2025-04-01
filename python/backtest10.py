import numpy as np
import pandas as pd
from binance.client import Client

# Binance API credentials (bu API anahtarları sadece örnek amaçlıdır, çalışmayacaktır)
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

def backtest_symbols(symbols, interval="1m", lookback=1440, vwap_offset=0.0015, 
                      take_profit_perc=0.0050, stop_loss_perc=0.0015, initial_balance=1000, leverage=10):
    results = []
    for symbol in symbols:
        try:
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
            quantity = (initial_balance * leverage) / 150  # Adjust quantity for $150 per trade

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

            results.append((symbol, balance - initial_balance))
        except Exception as e:
            print(f"Error processing symbol {symbol}: {e}")

    # Sort results by profit and return top 10 symbols
    results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
    return results

# Example usage
symbols_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]  # Replace with your symbols
results = backtest_symbols(symbols_list)

# Print top 10 symbols
print("Top 10 symbols by profit:")
for symbol, profit in results:
    print(f"{symbol}: ${profit:.2f}")
