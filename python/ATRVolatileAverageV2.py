import numpy as np
import pandas as pd
import ccxt
from talib import ATR

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
            'symbol': symbol,
            'current_atr_ratio': round(float(df['atr_ratio'].iloc[-1]),2),
            'average_atr_ratio': round(float(average_atr_ratio),2) if not np.isnan(average_atr_ratio) else None
        }
    return results

# Kullanımı:
symbols = ['BTC/USDT', 'ETH/USDT']
results = calculate_atr_volatility(symbols)

# Sonuçları DataFrame'e dönüştürme ve sıralama
df_results = pd.DataFrame(list(results.values()))
df_results.sort_values(by='average_atr_ratio', ascending=False, inplace=True)

# DataFrame'i sözlük listesine dönüştürme
sorted_results = df_results.to_dict('records')  # Her satırı bir sözlük olarak listeye dönüştürür

# Sıralı sonuçları yazdırma
print(sorted_results)
