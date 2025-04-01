import os
import time
from binance.client import Client
from binance import ThreadedWebsocketManager
import asyncio
import platform

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# API Anahtarlarınız
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Binance istemcisini oluşturun
client = Client(api_key, api_secret)

# Küresel değişkenler
long_candidates = []
total_buys = 0
total_sells = 0

def calculate_position_size(usdt_amount, leverage, price):
    return round((usdt_amount * leverage) / price, 3)

def order(side, quantity, symbol, order_type='MARKET'):
    try:
        print(f"Emir gönderiliyor: {side} {quantity} {symbol}")
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        print(response)
    except Exception as e:
        print(f"Emir hatası - {e}")

def close_all_positions():
    """Tüm açık pozisyonları kapatır."""
    positions = client.futures_position_information()
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = 'SELL' if float(position['positionAmt']) > 0 else 'BUY'
            quantity = abs(float(position['positionAmt']))
            order(side, quantity, position['symbol'])
    print("Tüm pozisyonlar kapatıldı.")

def get_open_positions():
    """Açık pozisyonları döndürür."""
    positions = client.futures_position_information()
    open_positions = {position['symbol']: float(position['positionAmt']) for position in positions if float(position['positionAmt']) > 0}
    return open_positions

def handle_depth_message(msg):
    global total_buys, total_sells, long_candidates

    # Mesajın formatını kontrol edin
    if 'e' not in msg or msg['e'] != 'depthUpdate' or 's' not in msg:
        return  # Beklenmeyen formatı atlayın

    symbol = msg['s']
    bids = msg['b']
    asks = msg['a']

    current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    lower_bound = current_price * 0.97
    upper_bound = current_price * 1.03

    total_bids = sum([float(bid[1]) for bid in bids if float(bid[0]) >= lower_bound])
    total_asks = sum([float(ask[1]) for ask in asks if float(ask[0]) <= upper_bound])

    buy_sell_ratio = total_bids / total_asks if total_asks > 0 else 0

    total_buys += total_bids
    total_sells += total_asks

    if buy_sell_ratio > 1.8 and symbol not in long_candidates:
        long_candidates.append(symbol)
        print(f"{symbol} longa aday, Alış/Satış Oranı: {buy_sell_ratio}")

def start_websocket(twm, symbols):
    """WebSocket'i başlatır ve sürekli çalışır."""
    try:
        for symbol in symbols:
            twm.start_depth_socket(callback=handle_depth_message, symbol=symbol.upper())
    except Exception as e:
        print(f"WebSocket hatası: {e}")

def main():
    global total_buys, total_sells, long_candidates
    coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']

    # Tek bir ThreadedWebsocketManager başlat
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()
    start_websocket(twm, coins)

    while True:
        long_candidates.clear()
        total_buys = 0
        total_sells = 0

        print("Veri toplama devam ediyor...")

        time.sleep(60)  # 60 saniye veri topla

        tcas = total_buys / total_sells if total_sells > 0 else 0
        print(f"TCAS Oranı: {tcas}")

        open_positions = get_open_positions()
        print(f"Açık Pozisyonlar: {open_positions}")

        if tcas > 1:
            print("TCAS 1'in üzerinde, long pozisyonlar açılıyor...")
            for symbol in long_candidates:
                if symbol.upper() not in open_positions:
                    price = float(client.get_symbol_ticker(symbol=symbol)['price'])
                    quantity = calculate_position_size(2.5, 6, price)
                    order('BUY', quantity, symbol.upper())
                else:
                    print(f"{symbol} için zaten açık pozisyon var.")
        else:
            print("TCAS 1'in altında, pozisyonlar kapatılıyor...")
            close_all_positions()

        print("Yeni tur başlıyor...\n")
        time.sleep(5)

if __name__ == "__main__":
    main()
