import time
from binance.client import Client
from binance.enums import *

api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'
client = Client(api_key, api_secret)

symbol = 'OMUSDT'

def get_price(symbol):
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

leverage = 5
investment = 3
quantity = investment * leverage / get_price(symbol)  # 60 dolar büyüklüğünde işlem miktarını hesapla
#quantity = 0.44500000  # Örnek miktar
precision = 8  # İzin verilen maksimum hassasiyet

# Miktarı izin verilen hassasiyete yuvarla
quantity = float(round(quantity, precision))


def open_short_position(symbol, quantity):
    order = client.futures_create_order(
        symbol=symbol,
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=quantity
    )
    return order

# Kaldıraç ayarla
client.futures_change_leverage(symbol=symbol, leverage=leverage)

highest_price = get_price(symbol)

while True:
    current_price = get_price(symbol)
    print("5sn")
    if current_price > highest_price:
        highest_price = current_price
    
    if current_price <= highest_price * 0.999:
        order = open_short_position(symbol, quantity)
        print(f"Short position opened at {current_price}")
        break
    
    time.sleep(5)  # Her 5 saniyede bir kontrol et

print(f"Highest price was {highest_price}")