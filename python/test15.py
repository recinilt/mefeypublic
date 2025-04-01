import time
from binance.client import Client
from binance.enums import *

api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

client = Client(api_key, api_secret)

symbol = 'HBARUSDT'
initial_price = float(client.get_symbol_ticker(symbol=symbol)['price'])

def get_price_change_percentage(initial, current):
    return ((current - initial) / initial) * 100

while True:
    current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    price_change = get_price_change_percentage(initial_price, current_price)
    
    if price_change >= 3:
        # Long pozisyon aç
        order = client.order_market_buy(
            symbol=symbol,
            quantity=50  # Miktarı ihtiyacınıza göre ayarlayın
        )
        print(f"Long pozisyon açıldı: {order}")
        initial_price = current_price  # Yeni başlangıç fiyatı olarak güncelle
    
    elif price_change <= -3:
        # Short pozisyon aç
        order = client.order_market_sell(
            symbol=symbol,
            quantity=50  # Miktarı ihtiyacınıza göre ayarlayın
        )
        print(f"Short pozisyon açıldı: {order}")
        initial_price = current_price  # Yeni başlangıç fiyatı olarak güncelle
    
    time.sleep(60)  # 1 dakika bekle ve tekrar kontrol et
