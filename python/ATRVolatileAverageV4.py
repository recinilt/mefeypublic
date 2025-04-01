import numpy as np
import pandas as pd
import ccxt
from talib import ATR
import time
import sys

# API anahtarları ve sembol listesi hazırlama
binance_api_key = "nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_api_secret = "WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"
from binance.client import Client
binanceclient = Client(binance_api_key, binance_api_secret)
exchange_info = binanceclient.futures_exchange_info()
time.sleep(2)
symbols = [s['symbol'] for s in exchange_info['symbols']]
symbols.sort()
#top_100_symbols=symbols[:100]
#print(top_100_symbols)
#print("Sembol sayısı: ", symbols, "Bizim bakacağımız ilk 100 coin.")


def fetch_data(symbol, timeframe='5m', limit=3000):
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol.replace('USDT', '/USDT'), timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def calculate_atr_volatility(symbols):
    results = []
    spinner = ['-', '\\', '|', '/']
    for index, symbol in enumerate(symbols):
        df = fetch_data(symbol)
        atr = ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)
        df['atr'] = atr
        df['atr_ratio'] = 100 * df['atr'] / df['close']
        average_atr_ratio = df['atr_ratio'].rolling(window=210).mean().iloc[-1]
        results.append([
            symbol,
            round(float(df['atr_ratio'].iloc[-1]), 2),
            round(float(average_atr_ratio) if not np.isnan(average_atr_ratio) else None, 2)
        ])
        sys.stdout.write('\r' + spinner[index % 4] + ' processing ' + symbol)
        sys.stdout.flush()
        
    sys.stdout.write('\rDone!                                       \n')
    # Sonuçları average_atr_ratio'ya göre büyükten küçüğe sırala
    results.sort(key=lambda x: x[2], reverse=True)
    return results

# Kullanımı:
#symbols = ['BTCUSDT', 'ETHUSDT']  # Örnek semboller
results = calculate_atr_volatility(symbols)

# Sonuçları yazdırma
print("symbol", "atr","average atr")
print(results)
