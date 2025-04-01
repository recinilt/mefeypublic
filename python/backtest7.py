import numpy as np
import pandas as pd
from itertools import product
from binance.client import Client
from tqdm import tqdm

# Binance API credentials
API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Fiyat verilerini Binance API'sinden yükleme
def fetch_data(symbol, interval, limit):
    candles = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close'] = data['close'].astype(float)
    data['volume'] = data['volume'].astype(float)
    data.set_index('timestamp', inplace=True)
    return data[-1440:]

symbol = "BTCUSDT"
interval = "1m"
limit = 1440

data = fetch_data(symbol, interval, limit)

# Parametre aralıkları
vwap_offsets = np.arange(0.0010, 0.0050, 0.0005)
take_profit_percs = np.arange(0.0010, 0.0150, 0.0005)
stop_loss_percs = np.arange(0.0010, 0.0050, 0.0005)

# Fonksiyonlar
def calculate_vwap(df):
    prices = df['close']
    volumes = df['volume']
    return np.sum(prices * volumes) / np.sum(volumes)

def backtest(data, vwap_offset, take_profit_perc, stop_loss_perc):
    vwap = calculate_vwap(data)
    long_entry = vwap * (1 + vwap_offset)
    short_entry = vwap * (1 - vwap_offset)

    balance = 10000  # Başlangıç bakiyesi
    trades = []

    for i in range(len(data)):
        close_price = data.iloc[i]['close']

        if close_price > long_entry:
            take_profit_price = close_price * (1 + take_profit_perc)
            stop_loss_price = close_price * (1 - stop_loss_perc)
            trades.append(("LONG", close_price, take_profit_price, stop_loss_price))

        elif close_price < short_entry:
            take_profit_price = close_price * (1 - take_profit_perc)
            stop_loss_price = close_price * (1 + stop_loss_perc)
            trades.append(("SHORT", close_price, take_profit_price, stop_loss_price))

    profit = len(trades) * (balance * (take_profit_perc - stop_loss_perc))
    return balance + profit, len(trades)

# Parametre kombinasyonlarını test etme
results = []
param_combinations = list(product(vwap_offsets, take_profit_percs, stop_loss_percs))

for vwap_offset, take_profit_perc, stop_loss_perc in tqdm(param_combinations, desc="Testing parameter combinations"):
    final_balance, trade_count = backtest(data, vwap_offset, take_profit_perc, stop_loss_perc)

    if trade_count > 0:  # İşlem yapmamış parametreleri ele
        results.append({
            'vwap_offset': vwap_offset,
            'take_profit_perc': take_profit_perc,
            'stop_loss_perc': stop_loss_perc,
            'final_balance': final_balance,
            'trade_count': trade_count
        })

# En iyi sonuçları sıralama
results = sorted(results, key=lambda x: x['final_balance'], reverse=True)[:50]

# Sonuçları ekrana yazdırma
print("Top 50 Results:")
for result in results:
    print(f"VWAP Offset: {result['vwap_offset']:.4f}, Take Profit: {result['take_profit_perc']:.4f}, Stop Loss: {result['stop_loss_perc']:.4f}, Final Balance: {result['final_balance']:.2f}, Trade Count: {result['trade_count']}")
