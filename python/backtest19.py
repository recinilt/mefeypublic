import pandas as pd
import numpy as np
from binance.client import Client

# Binance API bilgilerini girin
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Binance istemcisi
client = Client(API_KEY, API_SECRET)

def fetch_binance_data(symbol, interval, limit):
    """Binance'ten geçmiş verileri çeker"""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume", "ignore"
    ])
    data = data[["timestamp", "open", "high", "low", "close", "volume"]]
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='ms')
    data["close"] = data["close"].astype(float)
    return data

def calculate_ema(data, span):
    """EMA hesaplar"""
    return data.ewm(span=span, adjust=False).mean()

def backtest_strategy(data, short_ema_period, long_ema_period):
    """Çifte EMA strateji backtest"""
    # EMA'ları hesapla
    data['short_ema'] = calculate_ema(data['close'], short_ema_period)
    data['long_ema'] = calculate_ema(data['close'], long_ema_period)

    # İşlem değişkenleri
    position = 0  # Pozisyon (0: None, 1: Long)
    balance = 10000  # Başlangıç bakiyesi
    leverage = 5  # Kaldıraç 
    entry_price = 0
    trades = 0

    # İşlem stratejisi
    for i in range(len(data)):
        if data['short_ema'][i] > data['long_ema'][i] and position == 0:
            # Long pozisyon aç
            position = 1
            entry_price = data['close'][i]
            trades += 1

        elif data['short_ema'][i] < data['long_ema'][i] and position == 1:
            # Long pozisyon kapat
            balance += leverage * (data['close'][i] - entry_price)
            position = 0

    # Sonuçlar
    return balance, trades

# Veri çekme
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
limit = 1440

data = fetch_binance_data(symbol, interval, limit)

# Stratejiyi test et
short_ema = 27
long_ema = 147
final_balance, total_trades = backtest_strategy(data, short_ema, long_ema)

# Sonuçları yazdır
print(f"Son bakiye: ${final_balance:.2f}")
print(f"Toplam işlem sayısı: {total_trades}")
