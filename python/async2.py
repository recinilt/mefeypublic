import asyncio
import time
from binance.client import Client
from binance.enums import *
from binance.helpers import round_step_size

# Binance API Anahtarları reccirik2
API_KEY = "nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
API_SECRET = "WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"

client = Client(API_KEY, API_SECRET)

# Yardımcı Fonksiyonlar
async def get_symbols_with_usdt():
    """Binance'teki aktif USDT çiftlerini getir."""
    print("get_symbols_with_usdt fonksiyonu çalışmaya başladı.")
    exchange_info = client.futures_exchange_info()
    usdt_symbols = [
        s['symbol'] for s in exchange_info['symbols']
        if 'USDT' in s['symbol'] and s['status'] == 'TRADING'
    ]
    print(f"USDT çiftleri alındı: {usdt_symbols[:5]}...")  # İlk 5 sembolü yazdır
    return usdt_symbols

async def get_recent_klines(symbol, interval="1m", limit=2):
    """Belirli bir sembol için son 2 period verisini getir."""
    #print(f"get_recent_klines fonksiyonu çalışmaya başladı. Sembol: {symbol}")
    try:
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        #print(f"Son 2 Kline verisi alındı: {klines}")
        return klines
    except Exception as e:
        print(f"Hata: {symbol} - {e}")
        return None

async def calculate_percentage_change(klines):
    """Kline verilerindeki yüzdelik değişimi hesapla."""
    #print("calculate_percentage_change fonksiyonu çalışmaya başladı.")
    close_1 = float(klines[-2][4])  # Önceki kapanış
    close_2 = float(klines[-1][4])  # Son kapanış
    change = ((close_2 - close_1) / close_1) * 100
    print(f"Yüzdelik değişim: {change:.2f}%")
    return change

async def open_long_position(symbol, leverage=5, margin=2.1):
    """2.1 USDT teminat ile 5x kaldıraçla long pozisyon aç."""
    print(f"open_long_position fonksiyonu çalışmaya başladı. Sembol: {symbol}")
    
    # Leverage değişikliği
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    
    # Pozisyon büyüklüğünü hesapla
    position_value = margin * leverage  # 2.1 USDT * 5 (kaldıraç)
    
    # Teminatın doğruluğunu kontrol et
    if margin <= 0:
        print(f"Hata: Teminat 0 veya negatif. Teminat: {margin}")
        return
    
    # Pozisyon miktarını belirle: 1 USDT'lik işlemde, 1.0 lot = 1 USDT
    qty = round_step_size(position_value, 0.001)
    
    # Eğer hesaplanan miktar sıfır veya negatifse, işlemi atla
    if qty <= 0:
        print(f"Hata: Hesaplanan miktar sıfır veya negatif. Miktar: {qty}")
        return
    
    # Pozisyon açma
    try:
        client.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=qty
        )
        print(f"Long pozisyon açıldı: {symbol}, Miktar: {qty}, Pozisyon Büyüklüğü: {position_value} USDT")
    except Exception as e:
        print(f"Pozisyon açma hatası: {e}")


async def monitor_positions():
    """PNL'ye göre pozisyonları izle ve zarar edenleri kapat."""
    print("monitor_positions fonksiyonu çalışmaya başladı.")
    positions = client.futures_position_information()
    for position in positions:
        if float(position['positionAmt']) != 0:  # Pozisyon varsa
            pnl_percentage = float(position['unRealizedProfit']) / float(position['marginMaintAmount']) * 100
            if pnl_percentage < -0.5:  # %1.5 zarar
                client.futures_create_order(
                    symbol=position['symbol'],
                    side=SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=abs(float(position['positionAmt']))
                )
                print(f"Kapatılan pozisyon: {position['symbol']} - Zarar: {pnl_percentage:.2f}%")

# Asenkron Görevler
async def monitor_market():
    """Her 2 dakikada bir marketi kontrol eder."""
    print("monitor_market fonksiyonu çalışmaya başladı.")
    while True:
        usdt_symbols = await get_symbols_with_usdt()
        for symbol in usdt_symbols:
            klines = await get_recent_klines(symbol)
            if not klines:
                continue
            change = await calculate_percentage_change(klines)
            if change > 2.1:
                await open_long_position(symbol)
        print("async2.py")
        await asyncio.sleep(120)  # 2 dakikalık döngü

async def monitor_open_positions():
    """Her 15 saniyede bir açık pozisyonları kontrol eder."""
    print("monitor_open_positions fonksiyonu çalışmaya başladı.")
    while True:
        await monitor_positions()
        await asyncio.sleep(15)

# Ana Asenkron Döngü
async def main():
    print("Ana asenkron döngü çalışmaya başladı.")
    tasks = [
        asyncio.create_task(monitor_market()),
        asyncio.create_task(monitor_open_positions())
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
