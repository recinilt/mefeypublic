import pandas as pd
import numpy as np
from binance.client import Client
from talib import RSI, EMA, BBANDS
import datetime

# Binance API Anahtarlarınız
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Binance Client
client = Client(API_KEY, API_SECRET)

# Strateji Parametreleri
SYMBOL = "ETHUSDT"
INTERVAL = "5m"
LOOKBACK = "7 days ago UTC"  # Geriye dönük 7 gün
TRADE_AMOUNT = 100  # Başlangıç Bakiyesi (USDT)
TRADE_SIZE = 2  # Her işlemde kullanılacak miktar (USDT)

# Teknik Gösterge Parametreleri
BB_LENGTH = 20
BB_MULT = 2
RSI_PERIOD = 14
EMA_PERIOD = 20

# Fiyat Verilerini Çek

def fetch_data(symbol, interval, lookback):
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df = df[["open_time", "high", "low", "close", "volume"]]
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    return df

# Göstergeleri Hesapla

def calculate_indicators(df):
    df["RSI"] = RSI(df["close"], timeperiod=RSI_PERIOD)
    upper_band, middle_band, lower_band = BBANDS(df["close"], timeperiod=BB_LENGTH, nbdevup=BB_MULT, nbdevdn=BB_MULT)
    df["BB_UPPER"] = upper_band
    df["BB_MID"] = middle_band
    df["BB_LOWER"] = lower_band
    df["EMA"] = EMA(df["close"], timeperiod=EMA_PERIOD)
    return df

# Backtest Stratejisi

def backtest_strategy(df):
    balance = TRADE_AMOUNT
    trades = 0
    position = None
    entry_price = 0

    for i in range(len(df)):
        row = df.iloc[i]

        # Daha Esnek Long Koşulu
        if row["close"] <= row["BB_LOWER"] * 1.02 and row["RSI"] < 35 and row["close"] < row["EMA"] * 0.99 and position is None:
            position = "LONG"
            entry_price = row["close"]
            trades += 1
            print(f"LONG Açıldı: {entry_price} @ {row['open_time']}")

        # Daha Esnek Short Koşulu
        elif row["close"] >= row["BB_UPPER"] * 0.98 and row["RSI"] > 65 and row["close"] > row["EMA"] * 1.01 and position is None:
            position = "SHORT"
            entry_price = row["close"]
            trades += 1
            print(f"SHORT Açıldı: {entry_price} @ {row['open_time']}")

        # Pozisyon Kapatma
        if position == "LONG" and row["close"] >= row["BB_MID"]:
            profit = (row["close"] - entry_price) / entry_price * TRADE_SIZE
            balance += profit
            print(f"LONG Kapandı: {row['close']} @ {row['open_time']}, Kâr: {profit:.2f} USDT")
            position = None

        elif position == "SHORT" and row["close"] <= row["BB_MID"]:
            profit = (entry_price - row["close"]) / entry_price * TRADE_SIZE
            balance += profit
            print(f"SHORT Kapandı: {row['close']} @ {row['open_time']}, Kâr: {profit:.2f} USDT")
            position = None

    print(f"Toplam Bakiye: {balance:.2f} USDT")
    print(f"Toplam İşlem Sayısı: {trades}")


# Ana Program
if __name__ == "__main__":
    print("Veriler Çekiliyor...")
    data = fetch_data(SYMBOL, INTERVAL, LOOKBACK)
    print("Göstergeler Hesaplanıyor...")
    data = calculate_indicators(data)
    print("Backtest Başlıyor...")
    backtest_strategy(data)
