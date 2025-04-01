import ccxt
import time
import sys
from datetime import datetime
from statistics import mean

"""
# API anahtarları ve sembol listesi hazırlama
binance_api_key = "your_api_key"
binance_api_secret = "your_api_secret"
from binance.client import Client
binanceclient = Client(binance_api_key, binance_api_secret)
exchange_info = binanceclient.futures_exchange_info()
time.sleep(2)
symbols = [s['symbol'] for s in exchange_info['symbols']]
top_100_symbols = symbols[:100]
print("Sembol sayısı: ", len(symbols), "Bizim bakacağımız ilk 100 coin.")
"""

top_100_symbols=['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT',
 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 
'TRBUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'ENJUSDT', 'FLMUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LITUSDT', 'UNFIUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'BTCSTUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT']

def fetch_data(symbol, timeframe='5m', limit=3000):
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol.replace('USDT', '/USDT'), timeframe=timeframe, limit=limit)
    # Convert timestamp to datetime and structure data as a list of dictionaries
    formatted_data = [
        {'timestamp': datetime.fromtimestamp(bar[0] / 1000),
         'open': bar[1], 'high': bar[2], 'low': bar[3], 'close': bar[4], 'volume': bar[5]}
        for bar in bars
    ]
    return formatted_data

def calculate_true_range(high, low, previous_close):
    true_ranges = []
    for i in range(len(high)):
        current_high = high[i]
        current_low = low[i]
        if i == 0:
            # No previous close for the first element
            true_range = current_high - current_low
        else:
            true_range = max(current_high - current_low, abs(current_high - previous_close), abs(current_low - previous_close))
        true_ranges.append(true_range)
        previous_close = current_low  # update previous close to current close for next iteration
    return true_ranges

def calculate_atr(data, timeperiod=14):
    high = [d['high'] for d in data]
    low = [d['low'] for d in data]
    close = [d['close'] for d in data]
    true_ranges = calculate_true_range(high, low, close[0])
    atr = [mean(true_ranges[max(0, i-timeperiod+1):i+1]) for i in range(len(true_ranges))]
    return atr

def calculate_atr_volatility(symbols):
    results = []
    spinner = ['-', '\\', '|', '/']
    for index, symbol in enumerate(symbols):
        data = fetch_data(symbol)
        atr = calculate_atr(data)
        atr_ratio = [100 * a / d['close'] for a, d in zip(atr, data)]
        average_atr_ratio = mean(atr_ratio[-210:]) if len(atr_ratio) >= 210 else None
        results.append([
            symbol,
            round(atr_ratio[-1], 2) if atr_ratio else None,
            round(average_atr_ratio, 2) if average_atr_ratio else None
        ])
        sys.stdout.write('\r' + spinner[index % 4] + ' processing ' + symbol)
        sys.stdout.flush()
    sys.stdout.write('\rDone!                                       \n')
    
    # Doğru bir şekilde sıralama için
    results.sort(key=lambda x: x[2] if x[2] is not None else float('-inf'), reverse=True)
    return results

# Kullanımı:
symbols = ['BTCUSDT', 'ETHUSDT']  # Örnek semboller
results = calculate_atr_volatility(top_100_symbols)

# Sonuçları yazdırma
print(results)
