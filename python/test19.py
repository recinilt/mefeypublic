import re

# Metin örneği
text = """
Canlı olan coin sayısı:0 olduğu için piyasa iştahsız görünüyor Kurnaz Avcı Modülünün Size Seçtiği Güvenilir Olabilecek Coinler: ETH TS:1,1 MTS:1,0 PT:1,056 Dk:290✅ Kar:%0,5 🙂 Grafik (http://tradingview.com/chart/?symbol=BINANCE:ETHUSDT) BTC TS:1,7 MTS:1,2 PT:1,042 Dk:324✅ Kar:%7,3 😍 Grafik (http://tradingview.com/chart/?symbol=BINANCE:BTCUSDT) BCH TS:1,5 MTS:1,8 PT:1,047 Dk:190✅ Kar:%15,2 🤑 Grafik (http://tradingview.com/chart/?symbol=BINANCE:BCHUSDT) USDC TS:NULL MTS:1,0 PT:Pump Yok Dk:242✅ Kar:%0,1 🙂 Grafik (http://tradingview.com/chart/?symbol=BINANCE:USDCUSDT) FIL TS:0,9 MTS:1,1 PT:1,043 Dk:189✅ Kar:%0,2 🙂 Grafik (http://tradingview.com/chart/?symbol=BINANCE:FILUSDT) LTC TS:1,2 MTS:1,2 PT:1,034 Dk:166✅ Kar:%1,7 🙂 Grafik (http://tradingview.com/chart/?symbol=BINANCE:LTCUSDT) BEL TS:0,9 MTS:1,5 PT:1,008 Dk:166✅ Kar:%-1,9 🤕 Grafik (http://tradingview.com/chart/?symbol=BINANCE:BELUSDT) Kurnaz Avcı Mantığını Anlamak Dokunun /EKurnazAvci
"""

# Regex deseni
pattern = r'\b(\w+)\s+TS:'

# Eşleşmeleri bul
matches = re.findall(pattern, text)

# Her bir eşleşmeye USDT ekleyip yeni bir liste oluştur
usdt_list = [match + 'USDT' for match in matches]

# Listeyi yazdır
print(usdt_list)
