from binance.client import Client

api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'
client = Client(api_key, api_secret)

exchange_info = client.futures_exchange_info()
symbols = exchange_info['symbols']

def check_future_eligibility(symbol):
    for s in symbols:
        if s['symbol'] == symbol:
            return True
    return False

symbol = 'BTCUSDT'  # Kontrol etmek istediğiniz sembolü girin
is_eligible = check_future_eligibility(symbol)

if is_eligible:
    print(f"{symbol} future işlemleri için uygun.")
else:
    print(f"{symbol} future işlemleri için uygun değil.")