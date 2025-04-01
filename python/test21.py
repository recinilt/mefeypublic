from binance.client import Client
from binance.enums import *
import requests
import hmac
import hashlib
import time

# API anahtarlarınızı buraya ekleyin
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Binance Client oluşturun
client = Client(api_key, api_secret)

symbol = 'BTCUSDT'

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def calculate_amount(usdt_amount, price):
    return usdt_amount / price

def open_leverage_long(symbol, leverage, amount_usdt):
    # Kaldıraç ayarlama
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    
    # Margin modunu ayarlama (isolated)
    client.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
    
    # İşlem büyüklüğünü hesaplayın
    order_size = amount_usdt * leverage
    
    # Long pozisyon açma
    order = client.futures_create_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=order_size
    )
    return order

# Örnek kullanım
symbol = 'BTCUSDT'  # İşlem yapmak istediğiniz coin çifti
leverage = 10  # Kaldıraç
amount_usdt = calculate_amount(2,float(client.get_symbol_ticker(symbol=symbol)['price']))  # Harcanacak USDT miktarı

order = open_leverage_long(symbol, leverage, amount_usdt)
print(order)
