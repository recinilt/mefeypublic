import pandas as pd
import numpy as np
from binance.client import Client
import time

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

# Bollinger Band ve EMA Parametreleri
BB_LENGTH = 20
BB_MULT = 2
EMA9_LENGTH = 9
EMA21_LENGTH = 21

# Fiyat Verilerini Çek
def fetch_data(symbol, interval='1m', lookback='50'):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 
                                      'close_time', 'quote_asset_volume', 'trades', 
                                      'taker_buy_base', 'taker_buy_quote', 'ignore'])
    # Tüm gerekli sütunları float'a dönüştür
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df


# Göstergeleri Hesapla
def calculate_indicators(df):
    df['EMA9'] = df['close'].ewm(span=EMA9_LENGTH).mean()
    df['EMA21'] = df['close'].ewm(span=EMA21_LENGTH).mean()
    df['BB_MID'] = df['close'].rolling(BB_LENGTH).mean()
    df['BB_STD'] = df['close'].rolling(BB_LENGTH).std()
    df['BB_UPPER'] = df['BB_MID'] + BB_MULT * df['BB_STD']
    df['BB_LOWER'] = df['BB_MID'] - BB_MULT * df['BB_STD']
    df['VWAP'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

# Koşulları Kontrol Et
def check_conditions(df):
    last_row = df.iloc[-1]
    long_condition = (last_row['close'] <= last_row['BB_LOWER']) and \
                     (last_row['close'] > last_row['VWAP']) and \
                     (last_row['EMA9'] > last_row['EMA21'])
    short_condition = (last_row['close'] >= last_row['BB_UPPER']) and \
                      (last_row['close'] < last_row['VWAP']) and \
                      (last_row['EMA9'] < last_row['EMA21'])
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
