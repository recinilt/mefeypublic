import pandas as pd
import numpy as np
from tqdm import tqdm

# Parametreler
lowest_price = 7
highest_price = 300
grid_count = 1000
investment = 4300
slippage = 0.0001
commission = 0.001

def calculate_grids(lowest, highest, count, mode='geometric'):
    if mode == 'geometric':
        return np.geomspace(lowest, highest, num=count)
    else:
        return np.linspace(lowest, highest, num=count)

def simulate_grid_trading(df, grids, investment, slippage, commission):
    current_price = df['close'].iloc[0]
    coin_amount = 0
    usdt_balance = investment
    trade_results = []

    # Gridleri başlangıç fiyatına göre ayarla
    buy_grids = grids[grids < current_price]
    sell_grids = grids[grids > current_price]

    # İlk alımı yap
    for price in buy_grids[::-1]:
        if usdt_balance > 0:
            buy_amount = (investment / len(grids)) / price
            usdt_balance -= buy_amount * price * (1 + slippage + commission)
            coin_amount += buy_amount

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        current_price = row['close']

        # Satış işlemleri
        for price in sell_grids:
            if current_price >= price and coin_amount > 0:
                sell_amount = (investment / len(grids)) / price
                if sell_amount <= coin_amount:
                    coin_amount -= sell_amount
                    usdt_balance += sell_amount * price * (1 - slippage - commission)
                    trade_results.append((row['timestamp'], 'sell', sell_amount, price))
        
        # Alım işlemleri
        for price in buy_grids:
            if current_price <= price and usdt_balance > 0:
                buy_amount = (investment / len(grids)) / price
                usdt_balance -= buy_amount * price * (1 + slippage + commission)
                coin_amount += buy_amount
                trade_results.append((row['timestamp'], 'buy', buy_amount, price))

    return usdt_balance, coin_amount * current_price, trade_results

# CSV dosyasını yükle
df = pd.read_csv('SOLUSDT_1m.csv')
df['close'] = pd.to_numeric(df['close'])

# Gridleri hesapla
grids = calculate_grids(lowest_price, highest_price, grid_count, 'geometric')

# Ticareti simüle et
usdt_balance, coin_value_in_usdt, trades = simulate_grid_trading(df, grids, investment, slippage, commission)

print(f"Son USDT Bakiyesi: {usdt_balance:.2f} USDT")
print(f"Satılmamış Coin'lerin Değeri: {coin_value_in_usdt:.2f} USDT")
print(f"Toplam Sermaye: {(usdt_balance + coin_value_in_usdt):.2f} USDT")
