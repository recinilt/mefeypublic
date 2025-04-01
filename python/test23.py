from binance.client import Client

# Binance API Key ve Secret Key
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_SECRET_KEY'

# Binance client oluşturma
client = Client(api_key, api_secret)

# Belirli bir coinin fiyat bilgisini alma
symbol = 'BTCUSDT'  # BTC/USDT çifti
ticker = client.get_symbol_ticker(symbol=symbol)

# Fiyat bilgisini yazdırma
print(f"Fiyat: {ticker['price']}")
