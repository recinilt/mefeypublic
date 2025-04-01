import pandas as pd
import numpy as np
from binance.client import Client

# Binance API bilgileri (kendi API anahtarlarınızı girin)
api_key = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
api_secret = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Binance istemcisi
client = Client(api_key, api_secret)

def get_historical_data(symbol, interval, lookback):
    """Binance'ten geçmiş veri al."""
    klines = client.get_historical_klines(symbol, interval, f"{lookback} minutes ago UTC")
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'quote_asset_volume', 'number_of_trades',
                                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['close']].astype(float)
    return df

def calculate_ema(df, span):
    """EMA hesapla."""
    return df['close'].ewm(span=span, adjust=False).mean()

def backtest_ema_strategy(data, short_ema, long_ema):
    """EMA stratejisi ile backtest yap."""
    data['EMA_Short'] = calculate_ema(data, short_ema)
    data['EMA_Long'] = calculate_ema(data, long_ema)
    data['Signal'] = 0
    data.loc[data['EMA_Short'] > data['EMA_Long'], 'Signal'] = 1
    data.loc[data['EMA_Short'] <= data['EMA_Long'], 'Signal'] = -1

    # Pozisyon değişikliklerini bul (işlem noktaları)
    data['Position'] = data['Signal'].diff()

    # Performans hesaplama
    initial_balance = 1000  # Başlangıç bakiyesi (örnek)
    balance = initial_balance
    position = 0  # 0: Nakit, 1: Uzun pozisyon
    entry_price = 0
    trades = 0

    for i, row in data.iterrows():
        if row['Position'] == 1:  # Al sinyali
            if position == 0:
                entry_price = row['close']
                position = 1
                trades += 1
        elif row['Position'] == -1:  # Sat sinyali
            if position == 1:
                balance += (row['close'] - entry_price) / entry_price * balance
                position = 0

    # Son durumda pozisyon kapatma
    if position == 1:
        balance += (data['close'].iloc[-1] - entry_price) / entry_price * balance

    return balance, trades, data

# Parametreler
symbol = "BTCUSDT"  # İşlem çifti
interval = Client.KLINE_INTERVAL_1MINUTE  # Zaman dilimi
lookback = 1440  # Geçmiş periyot sayısı
short_ema = 27
long_ema = 147

# Veri al ve stratejiyi çalıştır
try:
    data = get_historical_data(symbol, interval, lookback)
    final_balance, total_trades, analyzed_data = backtest_ema_strategy(data, short_ema, long_ema)

    print(f"Başlangıç Bakiyesi: 1000 USD")
    print(f"Final Bakiye: {final_balance:.2f} USD")
    print(f"Toplam İşlem Sayısı: {total_trades}")
except Exception as e:
    print(f"Hata: {e}")
