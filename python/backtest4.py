import os
import datetime
import pandas as pd
import numpy as np
from binance.client import Client
from tqdm import tqdm

# Binance API Bağlantısı
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
client = Client(API_KEY, API_SECRET)

# 1. Veri Toplama

def fetch_ohlcv(symbol, interval, lookback):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data = data[['timestamp', 'close']]
    data['close'] = data['close'].astype(float)
    return data

btc_data = fetch_ohlcv("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, 1440)
eth_data = fetch_ohlcv("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, 1440)

def save_data(data, filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{filename}_{timestamp}.csv"
    
    #file_path = os.path.join("C:", "Users", "yenir", "OneDrive", "yedek", "Kodlamalar", "mefey", "public", "python", "backtest4.py")

    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

save_data(btc_data, "BTCUSDT_data")
save_data(eth_data, "ETHUSDT_data")

# 2. İşleme Dönüştürme

def resample_data(data, interval):
    data.set_index('timestamp', inplace=True)
    #resampled = data['close'].resample(interval).ohlc()
    resampled = data['close'].resample('3min').ohlc()
    resampled.reset_index(inplace=True)
    return resampled

btc_3min = resample_data(btc_data, '3T')
eth_3min = resample_data(eth_data, '3T')

# 3. Sinyal ve Strateji

def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

def backtest_strategy(btc_data, eth_data, short_ema, long_ema, order_ratio_threshold):
    btc_data['short_ema'] = calculate_ema(btc_data['close'], short_ema)
    btc_data['long_ema'] = calculate_ema(btc_data['close'], long_ema)
    
    btc_data['order_ratio'] = btc_data['close'] * order_ratio_threshold  # Placeholder for actual ratio calculation
    btc_data['buy_signal'] = (btc_data['short_ema'] > btc_data['long_ema']) & (btc_data['order_ratio'] > order_ratio_threshold)
    btc_data['sell_signal'] = ~btc_data['buy_signal']

    balance = 1000  # Initial balance in USDT
    eth_balance = 0
    
    for i in range(len(btc_data)):
        if btc_data['buy_signal'].iloc[i]:
            eth_balance += balance / eth_data['close'].iloc[i]
            balance = 0
        elif btc_data['sell_signal'].iloc[i] and eth_balance > 0:
            balance += eth_balance * eth_data['close'].iloc[i]
            eth_balance = 0

    return balance

# 4. Parametre Optimizasyonu

results = []
short_ema_range = range(5, 20)
long_ema_range = range(20, 50)
order_ratio_range = np.linspace(0.5, 2, 10)

for short_ema in tqdm(short_ema_range, desc="Short EMA"):
    for long_ema in long_ema_range:
        for order_ratio in order_ratio_range:
            final_balance = backtest_strategy(btc_3min, eth_3min, short_ema, long_ema, order_ratio)
            results.append((short_ema, long_ema, order_ratio, final_balance))

results_df = pd.DataFrame(results, columns=['Short EMA', 'Long EMA', 'Order Ratio', 'Final Balance'])
results_df.sort_values(by='Final Balance', ascending=False, inplace=True)

# 5. Progress Bar ve Çıktılar

top_results = results_df.head(50)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"strategy_results_{timestamp}.csv"
top_results.to_csv(output_file, index=False)
print(f"Top results saved to {output_file}")
print(top_results)
