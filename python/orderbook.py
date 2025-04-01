import requests

def get_order_book_depth(symbol, depth=1000):
    # Binance API'den order book verisini çekme
    url = f"https://api.binance.com/api/v3/depth"
    params = {
        'symbol': symbol.upper(),
        'limit': depth
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def calculate_order_sum(symbol, percentage_threshold=3):
    # Order book verilerini getir
    order_book = get_order_book_depth(symbol)
    asks = order_book['asks']  # Satış emirleri (fiyat, miktar)
    bids = order_book['bids']  # Alış emirleri (fiyat, miktar)

    # Mevcut fiyatı belirle (En düşük satış emri)
    current_price = float(asks[0][0])

    # Hedef fiyat aralıklarını hesapla
    upper_limit = current_price * (1 + percentage_threshold / 100)
    lower_limit = current_price * (1 - percentage_threshold / 100)

    # Belirlenen yüzdelik aralıklara göre emir miktarlarını topla
    ask_sum = sum(float(amount) for price, amount in asks if float(price) <= upper_limit)
    bid_sum = sum(float(amount) for price, amount in bids if float(price) >= lower_limit)

    return [ask_sum, bid_sum]

# Örnek kullanım: 'BTCUSDT' için emir toplamları
result = calculate_order_sum('BTCUSDT')
print("\nyüzde 3 aşağısına kadarki ALIŞ emirleri toplamı büyüklüğü: ", result[1], "\nyüzde 3 faslasına kadarki SATIŞ emirleri toplamı büyüklüğü: ", result[0],  "\n ALIŞ/SATIŞ oranı: ", round((result[1]/result[0]),2))
