import pandas as pd
import numpy as np
import time
from talib import SAR, RSI, MACD
import requests

# Pionex API Anahtarları
API_KEY = '8tsTtFcyiAt2y2pHBZ7ed1AZ24J1NAgdB75gtbGgfjYpuvwmCMu4iM5tqnJvWzVVqV'
API_SECRET = 'XgoKEi6Y3yZTXHIfgbBpwlwYhYXXcSfo21NOYsEzHgaX5RDNQCHjuyyo9SXmcsZn'
BASE_URL = 'https://api.pionex.com'

# Strateji Parametreleri
SYMBOL = 'BTC-USDT'
LEVERAGE = 6
TRADE_AMOUNT_USDT = 2
STOP_LOSS_PERCENT = 0.5 / 100

# Teknik Gösterge Parametreleri
SAR_STEP = 0.02
SAR_MAX = 0.2
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9



BASE_URL = 'https://api.pionex.com'

def send_request(method, endpoint, params=None, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': API_KEY  # API anahtarınızı buraya ekleyin
    }
    response = requests.request(method, url, headers=headers, params=params, json=data)
    return response.json()

def fetch_data(symbol, interval='1m', lookback=100):
    endpoint = "/v1/market/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': lookback
    }
    response = send_request("GET", endpoint, params=params)
    print(f"API Yanıtı: {response}")  # Yanıtı kontrol edin
    if 'data' in response and isinstance(response['data'], list):
        klines = response['data']
        df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df
    else:
        raise Exception(f"Fiyat verileri alınamadı: {response}")


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

# Pozisyon Açma
def open_position(symbol, side, amount_usdt):
    endpoint = "/v1/order"
    price = fetch_price(symbol)
    qty = round((amount_usdt * LEVERAGE) / price, 6)
    data = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": qty
    }
    response = send_request("POST", endpoint, data=data)
    print(f"{side} Pozisyon Açıldı: {response}")
    return price, qty

# Pozisyon Kapatma
def close_position(symbol, side, qty):
    endpoint = "/v1/order"
    data = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": qty
    }
    response = send_request("POST", endpoint, data=data)
    print(f"Pozisyon Kapatıldı: {response}")

# Fiyat Al
def fetch_price(symbol):
    endpoint = f"/v1/market/ticker"
    params = {"symbol": symbol}
    response = send_request("GET", endpoint, params=params)
    if 'data' in response:
        return float(response['data']['price'])
    else:
        raise Exception("Fiyat alınamadı")

# Ana İşlem Döngüsü
def run_strategy():
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
                current_price = fetch_price(SYMBOL)
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
