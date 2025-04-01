from binance.client import Client
import pandas as pd
import time

# Binance API anahtarlarınızı girin
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Binance client oluştur
client = Client(api_key, api_secret)

# USDT çiftlerini al
def usdtpairsgetir():
    exchange_info = client.futures_exchange_info()
    usdt_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['quoteAsset'] == 'USDT' and symbol['status'] == 'TRADING']
    return usdt_pairs

def get_ohlcv(symbol):
    # 5 dakikalık periodun 25 geriye dönük bilgilerini al
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=25)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    return df

def calculate_ema(df, short_period=14, long_period=25):
    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    return df

def find_crossing_coins(usdt_pairs):
    crossing_coins = []
    for pair in usdt_pairs:
        df = get_ohlcv(pair)
        df = calculate_ema(df)
        if df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1] and df['ema_short'].iloc[-2] <= df['ema_long'].iloc[-2]:
            crossing_coins.append(pair)
    return crossing_coins

# Kesişim noktası halindeki coinleri bul
#crossing_coins = find_crossing_coins(usdtpairsgetir())
#print(crossing_coins)

while True:
    # Kesişim noktası halindeki coinleri bul
    crossing_coins = find_crossing_coins(usdtpairsgetir())
    print(crossing_coins) 
    time.sleep(300)
       
