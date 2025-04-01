import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime
import time
from tqdm import tqdm

# Binance API ayarları
API_KEY = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
API_SECRET = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'
client = Client(API_KEY, API_SECRET)

# Veri Toplama

def get_historical_data(symbol, interval, lookback):
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                        'quote_asset_volume', 'number_of_trades',
                                        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = pd.to_numeric(df['close'])
    return df[['close']]

btc_data = get_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1440 minutes ago UTC")
eth_data = get_historical_data("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1440 minutes ago UTC")

# İşleme Dönüştürme

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

# Sinyal ve Strateji

def calculate_signal(data_btc, data_eth, short_ema, long_ema, order_ratio):
    data_btc['short_ema'] = calculate_ema(data_btc['close'], short_ema)
    data_btc['long_ema'] = calculate_ema(data_btc['close'], long_ema)
    data_btc['order_ratio'] = get_order_ratio("BTCUSDT")

    buy_signal = (data_btc['short_ema'] > data_btc['long_ema']) & (data_btc['order_ratio'] > order_ratio)
    sell_signal = ~buy_signal

    return buy_signal, sell_signal

def get_order_ratio(symbol):
    depth = client.get_order_book(symbol=symbol)
    bids = sum([float(order[1]) for order in depth['bids'][:10]])
    asks = sum([float(order[1]) for order in depth['asks'][:10]])
    return bids / asks

# Parametre Optimizasyonu

def optimize_parameters(btc_data, eth_data):
    results = []
    for short_ema in tqdm(range(5, 50, 5)):
        for long_ema in range(10, 200, 10):
            if short_ema >= long_ema:
                continue
            for order_ratio in np.arange(1.0, 5.0, 0.5):
                buy_signal, sell_signal = calculate_signal(btc_data, eth_data, short_ema, long_ema, order_ratio)
                final_balance, trade_count = backtest_strategy(buy_signal, sell_signal, eth_data)
                if trade_count > 0:
                    results.append((short_ema, long_ema, order_ratio, trade_count, final_balance))

    sorted_results = sorted(results, key=lambda x: x[4], reverse=True)[:50]
    return sorted_results

def backtest_strategy(buy_signal, sell_signal, eth_data):
    balance = 1000  # USD
    eth_balance = 0
    trade_count = 0
    for i in range(len(buy_signal)):
        if buy_signal.iloc[i] and balance > 0:
            eth_balance = balance / eth_data['close'].iloc[i]
            balance = 0
            trade_count += 1
        elif sell_signal.iloc[i] and eth_balance > 0:
            balance = eth_balance * eth_data['close'].iloc[i]
            eth_balance = 0
            trade_count += 1

    return balance, trade_count

# Sonuç Çıktıları

def save_results(results):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"results_{now}.csv"
    df = pd.DataFrame(results, columns=['Short EMA', 'Long EMA', 'Order Ratio', 'Trade Count', 'Final Balance'])
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
    print("Top 50 Results:")
    print(df.head(50))

# Main
if __name__ == "__main__":
    results = optimize_parameters(btc_data, eth_data)
    save_results(results)
