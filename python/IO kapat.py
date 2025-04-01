from binance.client import Client

# API anahtarlarınızı buraya girin
api_key = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
api_secret = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Binance client oluştur
client = Client(api_key, api_secret)

# Açık pozisyonları al
positions = client.futures_position_information()

# USDT çiftlerini filtrele
usdt_positions = [
    pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
]

# Pozisyonları yazdır
print("Açık USDT Çiftleri Pozisyonları:")
for pos in usdt_positions:
    print(f"Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
