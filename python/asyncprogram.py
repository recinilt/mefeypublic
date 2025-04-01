import asyncio
import requests
import time
from binance.client import Client
from binance.enums import *
import pandas as pd


# Binance API bilgileri
binance_api_key = "nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_key = "WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"

binance_client = Client(binance_api_key, binance_secret_key)

my_cost = 1
my_leverage = 11
symbol_trailing_prices = []
my_open_positions = []
trailing_percentage = 1
long_position_symbols = []


# Fiyat alma fonksiyonu
async def get_price(symbol):
    try:
        ticker = await asyncio.to_thread(binance_client.get_symbol_ticker, symbol=symbol.upper())
        return float(ticker['price'])
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None


# Long pozisyon açma
async def buy_position(symbol, leverage, amount):
    try:
        await asyncio.to_thread(binance_client.futures_change_leverage, symbol=symbol, leverage=leverage)
        quantity = round((amount * leverage) / await get_price(symbol), 3)
        order = await asyncio.to_thread(binance_client.futures_create_order, 
                                         symbol=symbol.upper(), 
                                         side=SIDE_BUY, 
                                         type=ORDER_TYPE_MARKET, 
                                         quantity=quantity)
        print(f"Long açıldı: {order}")
        if symbol not in long_position_symbols:
            long_position_symbols.append(symbol)
    except Exception as e:
        print(f"Error opening long position for {symbol}: {e}")


# Pozisyon kapatma
async def close_position(symbol):
    try:
        positions = await asyncio.to_thread(binance_client.futures_position_information, symbol=symbol)
        for position in positions:
            if float(position['positionAmt']) != 0:
                side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
                quantity = abs(float(position['positionAmt']))
                order = await asyncio.to_thread(binance_client.futures_create_order, 
                                                 symbol=symbol, 
                                                 side=side, 
                                                 type=ORDER_TYPE_MARKET, 
                                                 quantity=quantity)
                print(f"Pozisyon kapatıldı: {order}")
                if symbol in long_position_symbols:
                    long_position_symbols.remove(symbol)
    except Exception as e:
        print(f"Error closing position for {symbol}: {e}")


# İşlemleri kontrol eden ilk görev
async def monitor_positions():
    while True:
        try:
            positions = await asyncio.to_thread(binance_client.futures_account)
            positions_info = positions['positions']
            for position in positions_info:
                if float(position['positionAmt']) != 0:
                    symbol = position['symbol']
                    pnl = float(position['unrealizedProfit'])
                    print(f"{symbol} açık pozisyon, PnL: {pnl}")
                    if pnl < -1 * trailing_percentage:
                        await close_position(symbol)
            await asyncio.sleep(15)  # 15 saniyede bir kontrol
        except Exception as e:
            print(f"Error monitoring positions: {e}")


# Coin araştıran ikinci görev
async def search_coins_to_trade():
    while True:
        try:
            usdt_pairs = await asyncio.to_thread(fetch_usdt_pairs)
            for symbol in usdt_pairs:
                if symbol not in long_position_symbols:
                    await buy_position(symbol, my_leverage, my_cost)
            await asyncio.sleep(120)  # 2 dakikada bir kontrol
        except Exception as e:
            print(f"Error searching coins: {e}")


# Binance Futures pariteleri alma
def fetch_usdt_pairs():
    try:
        url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        exchange_info = requests.get(url).json()
        return [s['symbol'] for s in exchange_info['symbols'] if s['quoteAsset'] == 'USDT']
    except Exception as e:
        print(f"Error fetching USDT pairs: {e}")
        return []


# Ana döngü
async def main():
    task1 = asyncio.create_task(monitor_positions())
    task2 = asyncio.create_task(search_coins_to_trade())
    await asyncio.gather(task1, task2)


# Çalıştırma
asyncio.run(main())
