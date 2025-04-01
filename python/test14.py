import requests

# Binance API URL
url = "https://api.binance.com/api/v3/exchangeInfo"

# İstek gönder
response = requests.get(url)
data = response.json()

# BTCUSDT sembolü için hassasiyeti bul
for symbol in data['symbols']:
    if symbol['symbol'] == 'OMUSDT':
        print(f"BTCUSDT için fiyat hassasiyeti: {symbol['quotePrecision']}")
        print(f"BTCUSDT için miktar hassasiyeti: {symbol['baseAssetPrecision']}")
        break
