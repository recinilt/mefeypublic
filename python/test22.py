from binance.client import Client
from binance.enums import *

# Binance API bilgilerini buraya ekleyin
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Binance istemcisi oluştur
client = Client(api_key, api_secret)

def open_long_position(symbol, leverage=10, spend_amount=2):
    # Kaldıraç ayarla
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    
    # İzole marjin ayarla
    client.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
    
    # Pozisyon büyüklüğü hesapla
    quantity = spend_amount * leverage

    # Long pozisyon aç
    order = client.futures_create_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=quantity
    )
    print(f"{symbol} için long pozisyon açıldı: {order}")

# Örnek kullanım: HBARUSDT için long pozisyon aç
open_long_position('HBARUSDT')
