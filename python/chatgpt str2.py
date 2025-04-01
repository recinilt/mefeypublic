import pandas as pd
import numpy as np
from binance.client import Client
import time
from talib import SAR, RSI, MACD

# Binance API Anahtarlarınız
API_KEY = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
API_SECRET = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Binance Futures Client
client = Client(API_KEY, API_SECRET)

# Strateji Parametreleri
SYMBOL = 'BTCUSDT'
LEVERAGE = 12
TRADE_AMOUNT_USDT = 10  # Harcama: 2 USDT, Kaldıraçla 12 USDT pozisyon
STOP_LOSS_PERCENT = 0.5 / 100  # %0.5 Stop-Loss

# Teknik Gösterge Parametreleri
SAR_STEP = 0.02
SAR_MAX = 0.2
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Fiyat Verilerini Çek
def fetch_data(symbol, interval='1m', lookback='100'):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 
                                      'close_time', 'quote_asset_volume', 'trades', 
                                      'taker_buy_base', 'taker_buy_quote', 'ignore'])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

# Göstergeleri Hesapla
def calculate_indicators(df):
    df['SAR'] = SAR(df['high'], df['low'], acceleration=SAR_STEP, maximum=SAR_MAX)
    df['RSI'] = RSI(df['close'], timeperiod=RSI_PERIOD)
    macd, signal, _ = MACD(df['close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    df['MACD'] = macd
    df['Signal'] = signal
    df['Volume_Avg'] = df['volume'].rolling(10).mean()
    return df

# Koşulları Kontrol Et
def check_conditions(df):
    last_row = df.iloc[-1]
    long_condition = (last_row['close'] < last_row['SAR']) and \
                     (last_row['RSI'] > 30) and \
                     (last_row['MACD'] > last_row['Signal']) and \
                     (last_row['volume'] > last_row['Volume_Avg'] * 1.2)
    
    short_condition = (last_row['close'] > last_row['SAR']) and \
                      (last_row['RSI'] < 70) and \
                      (last_row['MACD'] < last_row['Signal']) and \
                      (last_row['volume'] > last_row['Volume_Avg'] * 1.2)
    return long_condition, short_condition

# Kaldıraç Ayarı
def set_leverage(symbol, leverage):
    client.futures_change_leverage(symbol=symbol, leverage=leverage)

# Long/Short Pozisyon Açma
def open_position(symbol, side, amount_usdt):
    price = float(client.futures_mark_price(symbol=symbol)['markPrice'])
    qty = round((amount_usdt * LEVERAGE) / price, 3)
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=qty
    )
    print(f"{side} Pozisyon Açıldı: {order}")
    return price, qty

# Pozisyonu Kapatma
def close_position(symbol, side, qty):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=qty
    )
    print(f"Pozisyon Kapatıldı: {order}")

# Ana İşlem Döngüsü
def run_strategy():
    set_leverage(SYMBOL, LEVERAGE)
    in_position = False
    position_side = None
    entry_price = 0
    position_qty = 0

    while True:
        try:
            data = fetch_data(SYMBOL)
            data = calculate_indicators(data)
            long_condition, short_condition = check_conditions(data)

            # Long Koşulu
            if long_condition and not in_position:
                entry_price, position_qty = open_position(SYMBOL, 'BUY', TRADE_AMOUNT_USDT)
                stop_loss = entry_price * (1 - STOP_LOSS_PERCENT)
                in_position = True
                position_side = 'BUY'

            # Short Koşulu
            elif short_condition and not in_position:
                entry_price, position_qty = open_position(SYMBOL, 'SELL', TRADE_AMOUNT_USDT)
                stop_loss = entry_price * (1 + STOP_LOSS_PERCENT)
                in_position = True
                position_side = 'SELL'

            # Pozisyonu Kapatma (Stop-Loss veya Kar Al)
            if in_position:
                current_price = float(client.futures_mark_price(symbol=SYMBOL)['markPrice'])
                if (position_side == 'BUY' and current_price <= stop_loss) or \
                   (position_side == 'SELL' and current_price >= stop_loss):
                    close_position(SYMBOL, 'SELL' if position_side == 'BUY' else 'BUY', position_qty)
                    in_position = False

            time.sleep(10)

        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)

# Stratejiyi Başlat
if __name__ == "__main__":
    run_strategy()
