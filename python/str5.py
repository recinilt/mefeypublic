import time
from binance.client import Client
from binance.enums import *
import pandas as pd

# Binance API credentials
API_KEY = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
API_SECRET = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

client = Client(API_KEY, API_SECRET)

# Strategy parameters
SHORT_MA_LENGTH = 10
LONG_MA_LENGTH = 50
SYMBOL = 'LDOUSDT'  # Replace with your desired trading pair
LEVERAGE = 15       # Leverage
BASE_INVESTMENT = 2 # USDT to use per trade

# Set leverage
client.futures_change_leverage(symbol=SYMBOL, leverage=LEVERAGE)

# Fetch symbol info to determine precision
def get_symbol_info(symbol):
    info = client.futures_exchange_info()
    for s in info['symbols']:
        if s['symbol'] == symbol:
            return {
                'price_precision': s['pricePrecision'],
                'quantity_precision': s['quantityPrecision']
            }
    return None

symbol_info = get_symbol_info(SYMBOL)
if not symbol_info:
    raise ValueError(f"Symbol {SYMBOL} not found!")

price_precision = symbol_info['price_precision']
quantity_precision = symbol_info['quantity_precision']

# Fetch historical data
def get_historical_data(symbol, interval, limit=100):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = pd.to_numeric(df['close'])
    return df

# Calculate moving averages and generate signals
def generate_signals(df):
    df['short_ma'] = df['close'].rolling(window=SHORT_MA_LENGTH).mean()
    df['long_ma'] = df['close'].rolling(window=LONG_MA_LENGTH).mean()
    
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy signal
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell signal
    return df

# Close existing position
def close_position():
    positions = client.futures_position_information()
    for pos in positions:
        if pos['symbol'] == SYMBOL and float(pos['positionAmt']) != 0:
            side = SIDE_SELL if float(pos['positionAmt']) > 0 else SIDE_BUY
            quantity = abs(float(pos['positionAmt']))
            client.futures_create_order(
                symbol=SYMBOL,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=round(quantity, quantity_precision)
            )
            print(f"Closed existing position: {side}, Quantity: {quantity}")

# Execute trade
def execute_trade(signal):
    close_position()  # Close any existing position before opening a new one

    latest_price = float(client.futures_symbol_ticker(symbol=SYMBOL)['price'])
    quantity = round(BASE_INVESTMENT * LEVERAGE / latest_price, quantity_precision)

    if signal == 1:  # Buy
        print("Placing buy order...")
        order = client.futures_create_order(
            symbol=SYMBOL,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print("Buy order placed:", order)
    elif signal == -1:  # Sell
        print("Placing sell order...")
        order = client.futures_create_order(
            symbol=SYMBOL,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print("Sell order placed:", order)

# Main trading loop
def trading_bot():
    in_position = False
    while True:
        try:
            print("Fetching historical data...")
            data = get_historical_data(SYMBOL, Client.KLINE_INTERVAL_5MINUTE)
            data = generate_signals(data)
            latest_signal = data['signal'].iloc[-1]

            if latest_signal == 1 and not in_position:
                execute_trade(1)
                in_position = True

            elif latest_signal == -1 and in_position:
                execute_trade(-1)
                in_position = True  # Stay in position for opposite direction

            time.sleep(300)  # Wait 5 minutes before the next iteration

        except Exception as e:
            print("Error:", e)
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    trading_bot()
