import numpy as np
import time
import random
from binance.client import Client
from binance.enums import * #SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC

api_key = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
api_secret = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

client=Client(api_key, api_secret)

def geometric_division(start, end, num_levels):
    """
    Belirli bir aralığı geometrik olarak bölerek seviyeleri döndürür.
    
    Args:
        start (float): Başlangıç değeri (aralığın alt sınırı).
        end (float): Bitiş değeri (aralığın üst sınırı).
        num_levels (int): Bölünmek istenen geometrik seviye sayısı.
    
    Returns:
        list: Geometrik seviyelerin bir listesi.
    """
    # Geometrik olarak logspace kullanarak aralığı bölüyoruz
    levels = np.geomspace(start, end, num_levels)
    return levels.tolist()

# Örnek kullanım
start = 0.02
end = 0.6
num_levels = 200

levels = geometric_division(start, end, num_levels)
levels=[round(level, 5) for level in levels]
print(levels)

def split_levels(levels, close):
    """
    Levels listesini ikiye böler: close'dan düşük olanlar ve yüksek olanlar.
    
    Args:
        levels (list): Geometrik seviyelerin bir listesi.
        close (float): Close değeri, seviyelere göre listeyi böler.
    
    Returns:
        tuple: (alinacaklar, satilacaklar) listeleri.
    """
    # En yakın elemanı bul ve sil
    closest_level = min(levels, key=lambda x: abs(x - close))
    gecicilevels=levels[:]
    gecicilevels.remove(closest_level)
    
    # Close değerine göre böl
    alinacaklar = [level for level in gecicilevels if level < close]
    satilacaklar = [level for level in gecicilevels if level > close]
    
    return alinacaklar, satilacaklar

# Örnek kullanım
close = 0.032
alinacaklar, satilacaklar = split_levels(levels, close)
old_alinacaklar=alinacaklar[:]
old_satilacaklar=satilacaklar[:]
print("Alinacaklar:", alinacaklar)
print("Satilacaklar:", satilacaklar)

def find_excess_items(old_list, new_list):
    """
    Yeni alinacaklar listesindeki, eski alinacaklar listesine göre fazla olan elemanları döndürür.
    
    Args:
        old_list (list): Eski alinacaklar listesi.
        new_list (list): Yeni alinacaklar listesi.
    
    Returns:
        list: Yeni alinacaklar listesindeki fazlalık elemanlar.
    """
    # Yeni listede olup eski listede olmayan elemanları bul
    excess_items = [item for item in new_list if item not in old_list]
    return excess_items

# Örnek kullanım
#old_alinacaklar = [0.02, 0.03, 0.04]
#new_alinacaklar = [0.02, 0.03, 0.04, 0.05, 0.06]
close = 0.05
new_alinacaklar, new_satilacaklar = split_levels(levels, close)

fazlalikalinacaklar = find_excess_items(old_alinacaklar, new_alinacaklar)
fazlaliksatilacaklar= find_excess_items(old_satilacaklar, new_satilacaklar)
print("Fazlalikalinacaklar:", fazlalikalinacaklar)
print("Fazlaliksatilacaklar:", fazlaliksatilacaklar)


####


def generate_random_number(start, end):
    """
    Belirli bir aralıkta rastgele bir sayı üretir.
    
    Args:
        start (float): Başlangıç değeri (aralığın alt sınırı).
        end (float): Bitiş değeri (aralığın üst sınırı).
    
    Returns:
        float: Rastgele üretilen sayı.
    """
    return random.uniform(start, end)

# Örnek kullanım
start = 0.02
end = 0.6

random_number = round(generate_random_number(start, end),5)
print("Rastgele Sayı:", random_number)


##############


#from binance.client import Client


def get_binance_orders(symbol):
    """
    Binance API kullanarak belirli bir sembol için alım ve satım emirlerini ayırır.
    
    Args:
        api_key (str): Binance API anahtarı.
        api_secret (str): Binance API gizli anahtarı.
        symbol (str): Sembol (ör. "ONEUSDT").
    
    Returns:
        tuple: (alemirleri, satemirleri) -> Alım ve satım emirlerinin fiyat listeleri.
    """
    global client
    #client = Client(api_key, api_secret)
    
    # Tüm açık emirleri al
    orders = client.get_open_orders(symbol=symbol)
    
    # Mevcut fiyatı al
    ticker = client.get_symbol_ticker(symbol=symbol)
    current_price = float(ticker['price'])
    
    # Emirleri ayır
    alemirleri = []
    satemirleri = []
    
    for order in orders:
        price = float(order['price'])
        side = order['side']  # "BUY" veya "SELL"
        
        if side == "BUY" and price > current_price:
            alemirleri.append(price)
        elif side == "SELL" and price < current_price:
            satemirleri.append(price)
    
    return alemirleri, satemirleri, current_price

# Örnek kullanım

symbol = "ONEUSDT"

alemirleri, satemirleri, current_price = get_binance_orders(symbol)

print("Al Emirleri (alemirleri):", alemirleri)
print("Sat Emirleri (satemirleri):", satemirleri)

###########

'''

def place_sell_order(symbol, price, quantity):
    """
    Binance API kullanarak bir satış limiti emri oluşturur.
    
    Args:
        api_key (str): Binance API anahtarı.
        api_secret (str): Binance API gizli anahtarı.
        symbol (str): Sembol (ör. "ONEUSDT").
        price (float): Satış fiyatı.
        quantity (float): Satış miktarı (ör. 500 ONE).
    
    Returns:
        dict: Emir bilgilerini içeren sözlük.
    """
    # Binance client'ı başlat
    #client = Client(api_key, api_secret)
    global client
    
    # Limit satış emri oluştur
    try:
        order = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,  # Emir iptal edilmeden aktif kalır
            price=format(price, '.8f'),  # Binance 8 ondalık hane ister
            quantity=format(quantity, '.8f')  # Binance 8 ondalık hane ister
        )
        print("Satış emri başarıyla oluşturuldu:", order)
        return order
    except Exception as e:
        print("Hata oluştu:", e)
        return None

# Örnek kullanım
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
symbol = "ONEUSDT"
price = 0.04  # Satış fiyatı
quantity = 500  # Satılacak miktar (500 ONE)

place_sell_order(symbol, price, quantity)

'''
##################

'''

def place_buy_order( symbol, price, quantity):
    """
    Binance API kullanarak bir alım limiti emri oluşturur.
    
    Args:
        api_key (str): Binance API anahtarı.
        api_secret (str): Binance API gizli anahtarı.
        symbol (str): Sembol (ör. "ONEUSDT").
        price (float): Alım fiyatı.
        quantity (float): Alım miktarı (ör. 500 ONE).
    
    Returns:
        dict: Emir bilgilerini içeren sözlük.
    """
    # Binance client'ı başlat
    #client = Client(api_key, api_secret)
    global client

    try:
        # Limit alım emri oluştur
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,  # Emir iptal edilene kadar aktif kalır
            price=format(price, '.8f'),  # Binance 8 ondalık hane ister
            quantity=format(quantity, '.8f')  # Binance 8 ondalık hane ister
        )
        print("Alım emri başarıyla oluşturuldu:", order)
        return order
    except Exception as e:
        print("Hata oluştu:", e)
        return None

# Örnek kullanım
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
symbol = "ONEUSDT"
price = 0.02  # Alım fiyatı
quantity = 500  # Alınacak miktar (500 ONE)

place_buy_order(api_key, api_secret, symbol, price, quantity)


'''


#############

while True:
    random_number = round(generate_random_number(0.04, 0.06),5)
    alemirleri, satemirleri, current_price = get_binance_orders("ONEUSDT")
    alinacaklar, satilacaklar = split_levels(levels, current_price)
    new_alinacaklar=alinacaklar[:]
    new_satilacaklar=satilacaklar[:]

    fazlalikalinacaklar = find_excess_items(alemirleri, new_alinacaklar)
    fazlaliksatilacaklar= find_excess_items(satemirleri, new_satilacaklar)

    print(current_price)
    if fazlalikalinacaklar:
        print("alınacaklar: ", fazlalikalinacaklar)
        for orderprice in fazlalikalinacaklar:
            #place_buy_order(symbol, orderprice, 10/orderprice)
            print("aşağıya al emri konuldu" , orderprice)
    if fazlaliksatilacaklar:
        print("satılacaklar: ", fazlaliksatilacaklar)
        for orderprice in fazlaliksatilacaklar:
            #place_sell_order(symbol, orderprice, 10/orderprice)
            print("yukarıya sat emri konuldu ",orderprice)
    #old_alinacaklar=new_alinacaklar[:]
    #old_satilacaklar=new_satilacaklar[:]
    
    time.sleep(10)



