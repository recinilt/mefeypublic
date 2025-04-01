from binance.client import Client
from binance.enums import *
import pandas as pd
import time

def initialize_binance_client(api_key, api_secret):
    return Client(api_key, api_secret)

def set_leverage(client, symbol, leverage):
    try:
        client.futures_change_leverage(symbol=symbol.replace('/', ''), leverage=leverage)
        print(f"Leverage set to {leverage}x for {symbol}")
    except Exception as e:
        print(f"Error setting leverage: {e}")

def get_precision(client, symbol):
    info = client.futures_exchange_info()
    for item in info['symbols']:
        if item['symbol'] == symbol.replace('/', ''):
            return {
                'quantity': item['quantityPrecision'],
                'price': item['pricePrecision']
            }
    return None

def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

def calculate_macd(data, short_window, long_window, signal_window):
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd = short_ema - long_ema
    signal = calculate_ema(macd, signal_window)
    hist = macd - signal
    return macd.iloc[-1], signal.iloc[-1], hist.iloc[-1]

def close_position(client, symbol):
    positions = client.futures_position_information()
    for pos in positions:
        if pos['symbol'] == symbol.replace('/', '') and float(pos['positionAmt']) != 0:
            side = SIDE_SELL if float(pos['positionAmt']) > 0 else SIDE_BUY
            quantity = abs(float(pos['positionAmt']))
            try:
                client.futures_create_order(
                    symbol=symbol.replace('/', ''),
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                print(f"Closed position for {symbol}")
            except Exception as e:
                print(f"Error closing position: {e}")

# Settings
symbol = "CRV/USDT"
leverage = 25
initial_amount = 2  # USDT to use
short_window = 12
long_window = 26
signal_window = 9
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

# Initialize Binance Client
client = initialize_binance_client(api_key, api_secret)
set_leverage(client, symbol, leverage)
precision = get_precision(client, symbol)

# Trading logic
while True:
    try:
        klines = client.futures_klines(symbol=symbol.replace('/', ''), interval='1m', limit=100)
        close_prices = [float(kline[4]) for kline in klines]

        macd, signal, hist = calculate_macd(pd.Series(close_prices), short_window, long_window, signal_window)
        quantity = round(initial_amount * leverage / close_prices[-1], precision['quantity'])

        positions = client.futures_position_information()
        current_position = next((p for p in positions if p['symbol'] == symbol.replace('/', '')), None)

        # Check if there is already an open position
        if current_position and float(current_position['positionAmt']) != 0:
            print("Position already open. Skipping...")
            time.sleep(60)
            continue

        if macd > signal and hist > 0:
            client.futures_create_order(
                symbol=symbol.replace('/', ''),
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(f"Opened LONG position for {symbol}")

        elif macd < signal and hist < 0:
            client.futures_create_order(
                symbol=symbol.replace('/', ''),
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(f"Opened SHORT position for {symbol}")

        time.sleep(60)

    except Exception as e:
        print(f"Error in trading loop: {e}")
