from binance.client import Client
from binance.enums import *

# Binance API bilgilerini buraya ekleyin
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Binance istemcisi oluştur
client = Client(api_key, api_secret)

def get_highest_price(symbol, interval, duration):
    # Veri toplama
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=duration)
    
    # En yüksek fiyatı bulma
    highest_price = max(float(kline[4]) for kline in klines)
    
    return highest_price

# Örnek kullanım
symbol = 'VANRYUSDT'
interval = '1m'  # 1 dakika veri
duration = 60  # 60 dakika veri

highest_price = get_highest_price(symbol, interval, duration)
print(f"{symbol} için 60 dakika içindeki en yüksek fiyat: {highest_price}")
