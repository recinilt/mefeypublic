import numpy as np
import pandas as pd
import ccxt
import time
import sys

top_100_symbols=['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT',
 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 
'TRBUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'ENJUSDT', 'FLMUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LITUSDT', 'UNFIUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'BTCSTUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT']

def fetch_data(symbol, timeframe='5m', limit=3000):
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol.replace('USDT', '/USDT'), timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def custom_atr(high, low, close, timeperiod=14):
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(window=timeperiod).mean()
    return atr

def calculate_atr_volatility(symbols):
    results = []
    spinner = ['-', '\\', '|', '/']
    for index, symbol in enumerate(symbols):
        df = fetch_data(symbol)
        atr = custom_atr(df['high'], df['low'], df['close'], timeperiod=14)
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
    results.sort(key=lambda x: x[2], reverse=True)
    return results

# Kullanımı:
symbols = ['BTCUSDT', 'ETHUSDT']  # Örnek semboller
results = calculate_atr_volatility(top_100_symbols)

# Sonuçları yazdırma
print(results)
