import numpy as np
import pandas as pd
import ccxt
from talib import ATR
import time
################binance sembol listesi

binance_api_reccirik2="nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_reccirik2="WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"
from binance.client import Client
from binance.enums import *
binanceclient = Client(binance_api_reccirik2, binance_secret_reccirik2)
exchange_info = binanceclient.futures_exchange_info()
time.sleep(2)
symbols = exchange_info['symbols']
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s['symbol'])
############################

def fetch_data(symbol, timeframe='5m', limit=1000):
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def calculate_atr_volatility(symbols):
    results = {}
    for symbol in symbols:
        df = fetch_data(symbol)
        atr = ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)
        df['atr'] = atr
        df['atr_ratio'] = 100 * df['atr'] / df['close']
        average_atr_ratio = df['atr_ratio'].rolling(window=70).mean().iloc[-1]
        results[symbol] = {
            'current_atr_ratio': float(df['atr_ratio'].iloc[-1]),
            'average_atr_ratio': float(average_atr_ratio) if not np.isnan(average_atr_ratio) else None
        }
    return results

# Kullanımı:
symbols = ['BTC/USDT', 'ETH/USDT']
results = calculate_atr_volatility(mysymbols3)

# Sonuçları DataFrame'e dönüştürme ve sıralama
df_results = pd.DataFrame(results).T  # T transpoze ile sütunları satırlara dönüştürür
df_results.sort_values(by='average_atr_ratio', ascending=False, inplace=True)

# Sonuçları yazdırma
print(df_results)
