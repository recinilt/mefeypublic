import pandas as pd
import numpy as np

def run_grid_bot(csv_file_path, lower_price, upper_price, num_grids, initial_investment, commission_rate):
    df = pd.read_csv(csv_file_path)
    prices = df['close'].astype(float)

    # Grid hesaplamaları
    grid_size = (upper_price - lower_price) / num_grids
    grid_levels = np.linspace(lower_price, upper_price, num_grids + 1)
    grid_positions = {price: 0 for price in grid_levels}
    capital = initial_investment
    coins_held = 0
    transaction_log = []

    # İşlemleri başlat
    for price in prices:
        if price < lower_price or price > upper_price:
            continue

        # Uygun grid seviyesini bul
        level_index = np.searchsorted(grid_levels, price, side='right') - 1
        target_buy_price = grid_levels[level_index]
        target_sell_price = grid_levels[level_index + 1] if level_index + 1 <= num_grids else None

        # Alım yap
        if coins_held == 0 or price == target_buy_price:
            coins_to_buy = capital / price
            coins_held += coins_to_buy
            capital -= coins_to_buy * price
            capital -= coins_to_buy * price * commission_rate  # Komisyon kesintisi
            transaction_log.append((price, 'buy', coins_to_buy, capital, coins_held))
        
        # Satım yap
        elif price == target_sell_price:
            capital += coins_held * price
            capital -= coins_held * price * commission_rate  # Komisyon kesintisi
            transaction_log.append((price, 'sell', coins_held, capital, 0))
            coins_held = 0

    # Henüz satılmamış coin'lerin değeri
    unsold_coins_value = coins_held * prices.iloc[-1]

    # Toplam değer hesaplama
    total_value = capital + unsold_coins_value

    # Log ve toplam değeri döndür
    return transaction_log, total_value

# Parametreler
csv_file_path = 'BTCUSDT_1m.csv'
lower_price = 40000
upper_price = 150000
num_grids = 330
initial_investment = 100000
commission_rate = 0.001  # %0.1 komisyon

# Botu çalıştır
transaction_log, total_value = run_grid_bot(csv_file_path, lower_price, upper_price, num_grids, initial_investment, commission_rate)

# Sonuçları yazdır
for log in transaction_log:
    print(log)
print("Total value:", total_value)
