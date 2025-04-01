import datetime
import math
from binance.client import Client

# Binance API bilgilerinizi burada girin
api_key = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
api_secret = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
client = Client(api_key, api_secret)

def get_historical_data(symbol, interval, lookback):
    candles = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    data = []
    for candle in candles:
        data.append({
            "time": datetime.datetime.fromtimestamp(candle[0] / 1000),
            "close": float(candle[4]),
        })
    return data

def calculate_ema(prices, period):
    ema = []
    multiplier = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i < period - 1:
            ema.append(None)  # Yeterli veri yoksa EMA hesaplanamaz
        elif i == period - 1:
            ema.append(sum(prices[:period]) / period)
        else:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema

def simulate_trading(btc_data, buy_ratio, short_ema_period, long_ema_period):
    prices = [d["close"] for d in btc_data]
    short_ema = calculate_ema(prices, short_ema_period)
    long_ema = calculate_ema(prices, long_ema_period)

    balance = 1000  # Başlangıç bakiyesi
    btc_balance = 0
    last_signal = None
    trades = []

    for i in range(len(prices)):
        if i < long_ema_period - 1:
            continue  # Yeterli veri yoksa atla

        if short_ema[i] is None or long_ema[i] is None:
            continue

        current_price = prices[i]

        buy_signal = (buy_ratio > 1) and (short_ema[i] > long_ema[i])
        sell_signal = not buy_signal

        if buy_signal and last_signal != "BUY":
            btc_balance = balance / current_price
            balance = 0
            last_signal = "BUY"
            trades.append(("BUY", btc_data[i]["time"], current_price))

        elif sell_signal and last_signal == "BUY":
            balance = btc_balance * current_price
            btc_balance = 0
            last_signal = "SELL"
            trades.append(("SELL", btc_data[i]["time"], current_price))

    final_balance = balance + btc_balance * prices[-1]
    return final_balance, trades

def optimize_parameters(btc_data):
    best_results = []

    for buy_ratio in [1.1, 1.2, 1.3, 1.4, 1.5]:
        for short_ema_period in range(5, 20, 5):
            for long_ema_period in range(20, 60, 10):
                final_balance, trades = simulate_trading(
                    btc_data, buy_ratio, short_ema_period, long_ema_period
                )
                if trades:  # İşlem yapılmışsa değerlendir
                    best_results.append((
                        final_balance,
                        len(trades),
                        short_ema_period,
                        long_ema_period,
                        buy_ratio,
                    ))

    best_results.sort(reverse=True, key=lambda x: x[0])  # Bakiyeye göre sıralama
    return best_results[:5]

# Verileri çek
btc_data = get_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, 1440)
eth_data = get_historical_data("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, 1440)

# BTC ve ETH verilerini dosyalara kaydet
btc_filename = datetime.datetime.now().strftime("btc_data_%Y%m%d_%H%M%S.csv")
eth_filename = datetime.datetime.now().strftime("eth_data_%Y%m%d_%H%M%S.csv")

with open(btc_filename, "w") as f:
    f.write("time,close\n")
    for data in btc_data:
        f.write(f"{data['time']},{data['close']}\n")

with open(eth_filename, "w") as f:
    f.write("time,close\n")
    for data in eth_data:
        f.write(f"{data['time']},{data['close']}\n")

# Parametre optimizasyonu
best_parameters = optimize_parameters(btc_data)

print("En iyi 5 sonuç:")
for result in best_parameters:
    print(
        f"Bakiye: {result[0]:.2f}, İşlem Sayısı: {result[1]}, Kısa EMA: {result[2]}, Uzun EMA: {result[3]}, Emir Oranı: {result[4]}"
    )
