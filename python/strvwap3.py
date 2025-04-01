import time
import numpy as np
from binance.client import Client
from binance.enums import *
import os

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
binance_api_abim="W0cyfW6O27i7GsBKFYbm4zVjiOE0oY2lbOZYQwbYWksuDZG1zwt10x5w42GQ6JDa"
binance_secret_abim="FdrwJZG7zXTi3qwj9zQaxCb0YFWoYAZexGCTAP2QkUcMhV4dQuq5OGSQYgiQYioE"

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)
client.futures_change_leverage(symbol="BTCUSDT", leverage=125)
try:
    client.futures_change_margin_type(symbol="BTCUSDT", marginType='ISOLATED')
except Exception as e:
    print(e)
client_abim = Client(binance_api_abim, binance_secret_abim)
client_abim.futures_change_leverage(symbol="BTCUSDT", leverage=125)
try:
    client_abim.futures_change_margin_type(symbol="BTCUSDT", marginType='ISOLATED')
except Exception as e:
    print(e)

# Parameters
symbol = "BTCUSDT"  # Futures trading pair
interval = "1m"  # 1-minute interval
vwap_offset = 0.0016  # 0.16%
take_profit_perc = 0.0138  # 1.38%
stop_loss_perc = 0.006  # 0.6%
quantity = 0.005  # Adjust based on balance and risk

# Variables to track open positions
has_open_position = False
position = {
    'side': None,  # "BUY" or "SELL"
    'entry_price': None,
    'stop_loss_price': None,
    'take_profit_price': None
}

previous_close = None  # Track previous close price

# Function to calculate VWAP
def calculate_vwap(candles):
    prices = np.array([float(c[4]) for c in candles])  # Close prices
    volumes = np.array([float(c[5]) for c in candles])  # Volumes
    return np.sum(prices * volumes) / np.sum(volumes)

# Function to place an order
def place_order(order_side, price, stop_price, take_profit_price):
    global has_open_position, position
    try:
        # Place market order
        order = client.futures_create_order(
            symbol=symbol,
            side=order_side,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"{order_side.capitalize()} order placed: {order}")
        
        # Update position details
        has_open_position = True
        position.update({
            'side': order_side,
            'entry_price': price,
            'stop_loss_price': stop_price,
            'take_profit_price': take_profit_price
        })

        # Log details
        print(f"Details: Side={order_side}, Price={price}, Stop Price={stop_price}, Take Profit={take_profit_price}")

    except Exception as e:
        print(f"Error placing order: {e}")

    try:
        # Place market order for second account
        order2 = client_abim.futures_create_order(
            symbol=symbol,
            side=order_side,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"{order_side.capitalize()} order placed: {order2}")

    except Exception as e:
        print(f"Error placing order: {e}")

# Function to monitor open position
def monitor_position(current_price):
    global has_open_position, position

    if not has_open_position:
        return

    # Long position
    if position['side'] == "BUY":
        if current_price <= position['stop_loss_price']:
            print(f"Stop-loss triggered for LONG at {current_price:.2f}")
            close_position()
        elif current_price >= position['take_profit_price']:
            print(f"Take-profit triggered for LONG at {current_price:.2f}")
            close_position()

    # Short position
    elif position['side'] == "SELL":
        if current_price >= position['stop_loss_price']:
            print(f"Stop-loss triggered for SHORT at {current_price:.2f}")
            close_position()
        elif current_price <= position['take_profit_price']:
            print(f"Take-profit triggered for SHORT at {current_price:.2f}")
            close_position()

# Function to close position
def close_position():
    global has_open_position, position
    try:
        # Place market order to close the position
        client.futures_create_order(
            symbol=symbol,
            side="SELL" if position['side'] == "BUY" else "BUY",
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Position closed: {position}")
        has_open_position = False
        position = {'side': None, 'entry_price': None, 'stop_loss_price': None, 'take_profit_price': None}
    except Exception as e:
        print(f"Error closing position: {e}")

    try:
        # Place market order for second account
        client_abim.futures_create_order(
            symbol=symbol,
            side="SELL" if position['side'] == "BUY" else "BUY",
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Position closed: {position}")
    except Exception as e:
        print(f"Error closing position: {e}")

# Function to display status
def display_status(vwap, close_price, long_entry_level, short_entry_level, long_condition, short_condition):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Symbol: {symbol}")
    print(f"VWAP: {vwap:.2f}")
    print(f"Close Price: {close_price:.2f}")
    print(f"Long Entry Level: {long_entry_level:.2f}")
    print(f"Short Entry Level: {short_entry_level:.2f}")
    print(f"Long Condition: {'Triggered' if long_condition else 'Not Triggered'}")
    print(f"Short Condition: {'Triggered' if short_condition else 'Not Triggered'}")
    print(f"Open Position: {'Yes' if has_open_position else 'No'}")

# Countdown timer
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"Next check in {remaining} seconds...", end="\r")
        time.sleep(1)

# Main trading loop
while True:
    try:
        # Fetch recent candles
        candles = client.futures_klines(symbol=symbol, interval=interval, limit=20)

        # Calculate VWAP
        vwap = calculate_vwap(candles)

        # Get the latest close price
        close_price = float(candles[-1][4])

        # Calculate entry levels
        long_entry_level = vwap * (1 + vwap_offset)
        short_entry_level = vwap * (1 - vwap_offset)

        # Check if no open position
        if not has_open_position:
            #global previous_close

            # Long condition (cross above)
            long_condition = previous_close and (previous_close <= long_entry_level and close_price > long_entry_level)
            if long_condition:
                take_profit_price = close_price * (1 + take_profit_perc)
                stop_loss_price = close_price * (1 - stop_loss_perc)
                place_order("BUY", close_price, stop_loss_price, take_profit_price)

            # Short condition (cross below)
            short_condition = previous_close and (previous_close >= short_entry_level and close_price < short_entry_level)
            if short_condition:
                take_profit_price = close_price * (1 - take_profit_perc)
                stop_loss_price = close_price * (1 + stop_loss_perc)
                place_order("SELL", close_price, stop_loss_price, take_profit_price)

        # Monitor open position
        monitor_position(close_price)

        # Update previous close price
        previous_close = close_price

        # Display status
        display_status(vwap, close_price, long_entry_level, short_entry_level, long_condition, short_condition)

        # Countdown before the next iteration
        countdown_timer(10)

    except Exception as e:
        print(f"Error in main loop: {e}")
        countdown_timer(10)
