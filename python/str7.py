import requests
import time
import hmac
import hashlib
import urllib.parse

# Binance API endpoint
BASE_URL = "https://api.binance.com/api/v3/"

# API Key ve Secret
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Pozisyon durumları
long_position = False
short_position = False
initial_quantity = 2  # Başlangıç pozisyon büyüklüğü (USDT)
current_quantity = initial_quantity  # Mevcut pozisyon büyüklüğü
leverage = 15  # Kaldıraç
symbol = "SUSHIUSDT"  # İşlem çifti
precision = None  # Precision bilgisi

# Binance API'den precision bilgisi al
def fetch_precision(symbol):
    url = f"{BASE_URL}exchangeInfo"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    for s in data['symbols']:
        if s['symbol'] == symbol:
            for f in s['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    return int(abs(round(-1 * (float(f['stepSize']))).as_integer_ratio()[1]))
    return 2  # Default precision

# Binance API'den veri çekme
def fetch_klines(symbol, interval, limit):
    url = f"{BASE_URL}klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [float(kline[4]) for kline in response.json()]  # Kapanış fiyatlarını al

# Binance pozisyon açma
def place_order(symbol, side, quantity):
    url = f"{BASE_URL}order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    query_string = urllib.parse.urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    params["signature"] = signature
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"Order placed successfully: {side} {quantity} {symbol}")
    else:
        print(f"Order failed: {response.json()}")

# Fonksiyon: EMA hesaplama
def calculate_ema(data, period):
    ema_values = []
    multiplier = 2 / (period + 1)
    for i in range(len(data)):
        if i < period - 1:
            ema_values.append(None)  # İlk "period - 1" veri yok
        elif i == period - 1:
            sma = sum(data[:period]) / period  # İlk EMA için SMA
            ema_values.append(sma)
        else:
            ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)
    return ema_values

# Scalping stratejisi
def scalping_strategy(symbol, interval, short_period=5, long_period=25):
    global long_position, short_position, initial_quantity, current_quantity, precision
    
    if precision is None:
        precision = fetch_precision(symbol)

    data = fetch_klines(symbol, interval, max(short_period, long_period) + 1)
    short_ema = calculate_ema(data, short_period)
    long_ema = calculate_ema(data, long_period)

    if not short_ema[-2] or not long_ema[-2]:
        return ["yok", "yok"]  # Yeterli veri yok

    # Son iki EMA değerlerini kontrol et
    prev_short, prev_long = short_ema[-2], long_ema[-2]
    curr_short, curr_long = short_ema[-1], long_ema[-1]

    long_status = "yok"
    short_status = "yok"
    
    trade_quantity = round(current_quantity * leverage, precision)

    # Long ve Short Reverse Mantığı
    if long_position:
        if prev_short > prev_long and curr_short <= curr_long:
            long_status = "longexit"
            short_status = "shortac"
            short_position = True
            long_position = False
            current_quantity = initial_quantity * 2
            place_order(symbol, "SELL", trade_quantity)
    elif short_position:
        if prev_short < prev_long and curr_short >= curr_long:
            short_status = "shortexit"
            long_status = "longac"
            long_position = True
            short_position = False
            current_quantity = initial_quantity * 2
            place_order(symbol, "BUY", trade_quantity)
    else:
        if prev_short <= prev_long and curr_short > curr_long:
            long_status = "longac"
            long_position = True
            place_order(symbol, "BUY", trade_quantity)
        elif prev_short >= prev_long and curr_short < curr_long:
            short_status = "shortac"
            short_position = True
            place_order(symbol, "SELL", trade_quantity)

    return [long_status, short_status, trade_quantity]

# Her dakika stratejiyi kontrol etme
def main():
    global precision
    interval = "1m"  # 1 dakikalık grafik
    precision = fetch_precision(symbol)
    while True:
        result = scalping_strategy(symbol, interval)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Strateji Sonucu: {result}")
        time.sleep(60)  # 1 dakika bekle

if __name__ == "__main__":
    main()
