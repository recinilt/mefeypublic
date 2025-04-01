import numpy as np
import time
import random
from binance.client import Client
from binance.enums import * #SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from tqdm import tqdm
from decimal import Decimal
import math
import pandas as pd


api_key = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
api_secret = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

client=Client(api_key, api_secret)



levels=[]
geometric_percentage=1.1

symbol = ""
start = 1.1
end = 1.1
num_levels = 1
comission=1.1
minmiktarondalik=1
myticksize=1
precision_info={}
close = 0.032


def get_first_close(file_path):
    """
    Verilen CSV dosyasındaki ilk 'close' fiyatını döndürür.
    
    Args:
        file_path (str): CSV dosyasının yolu.
        
    Returns:
        float: İlk 'close' fiyatı.
    """
    try:
        # CSV dosyasını oku
        data = pd.read_csv(file_path)
        
        # 'close' sütununu kontrol et
        if 'close' in data.columns:
            # İlk 'close' fiyatını al
            first_close = data['close'].iloc[0]
            return first_close
        else:
            raise ValueError("'close' sütunu bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")
        return None

# Örnek kullanım
file_path = 'SOLUSDT_1m.csv'  # CSV dosyasının yolu
close = get_first_close(file_path)
if close is not None:
    print(f"İlk 'close' fiyatı: {close}")

def girdiler():
    global symbol
    global start
    global end
    global num_levels
    global comission
    global levels
    global geometric_percentage
    global minmiktarondalik
    global myticksize
    global precision_info
    global close
    symbol = input("Coin Çiftini Giriniz (Örn: BTCUSDT): ").upper()
    start = float(input("Alt seviyeyi giriniz (Örn: 0.02): "))
    end = float(input("Üst seviyeyi giriniz (Örn: 0.6): "))
    num_levels = int(input("Grid sayısını giriniz (Örn: 200): "))
    comission=float(input("Komisyon (Örn: %0.1 (yani binde bir)): %"))
    
    minmiktarondalik,myticksize,precision_info=get_precision(symbol)
    levels, geometric_percentage = geometric_division(start, end, num_levels)

def count_decimal_places(number):
    """
    Bir float sayının noktadan sonraki matematiksel anlamlı basamak sayısını döndürür.
    
    Args:
        number (float): Kontrol edilecek sayı.
    
    Returns:
        int: Noktadan sonraki anlamlı basamak sayısı.
    """
    # Decimal sınıfını kullanarak sayıyı işleme al
    number = Decimal(str(number)).normalize()  # Normalize ile gereksiz sıfırları kaldır
    if '.' in str(number):  # Eğer nokta varsa
        return abs(number.as_tuple().exponent)  # Ondalık basamak sayısını döndür
    return 0


def get_precision(symbol):
    """
    Binance API kullanarak bir coinin precision değerlerini alır.
    
    Args:
        api_key (str): Binance API anahtarı.
        api_secret (str): Binance API gizli anahtarı.
        symbol (str): İşlem çifti (ör. "ONEUSDT").
    
    Returns:
        dict: Precision bilgilerini içeren sözlük.
    """
    # Binance client'ı başlat
    #client = Client(api_key, api_secret)
    global client
    try:
        # Exchange bilgilerini al
        exchange_info = client.get_exchange_info()
        
        # İlgili sembolün bilgilerini bul
        for s in exchange_info['symbols']:
            if s['symbol'] == symbol:
                precision_info = {
                    'baseAssetPrecision': s['baseAssetPrecision'],  # Coin miktar hassasiyeti
                    'quoteAssetPrecision': s['quoteAssetPrecision'],  # USDT veya BTC hassasiyeti
                    'stepSize': None,  # Minimum miktar adımı
                    'tickSize': None   # Minimum fiyat adımı
                }
                # Emir hassasiyetlerini al
                for filt in s['filters']:
                    if filt['filterType'] == 'LOT_SIZE':
                        precision_info['stepSize'] = filt['stepSize']
                    if filt['filterType'] == 'PRICE_FILTER':
                        precision_info['tickSize'] = filt['tickSize']
                minmiktarondalik=count_decimal_places(precision_info["stepSize"])
                myticksize=count_decimal_places(precision_info["tickSize"])
                return minmiktarondalik,myticksize,precision_info
        
        # Sembol bulunamazsa
        print(f"{symbol} çifti bulunamadı.")
        return None
    except Exception as e:
        print("Hata oluştu:", e)
        return None




def geometric_division(start, end, num_levels):
    global myticksize
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
    levels = np.geomspace(start, end, num_levels).tolist()
    levels=[round(level, myticksize) for level in levels]
    # Geometrik yüzdeyi hesapla
    geometric_percentage = ((levels[1] - levels[0]) / levels[0]) * 100 if len(levels) > 1 else 0
    
    
    return levels, round(geometric_percentage,2)

# Örnek kullanım

girdiler()




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

alinacaklar, satilacaklar = split_levels(levels, close)
old_alinacaklar=alinacaklar[:]
old_satilacaklar=satilacaklar[:]
#print("Alinacaklar:", alinacaklar)
#print("Satilacaklar:", satilacaklar)

print("Precision bilgileri:", minmiktarondalik)

#print(levels)
myqs=0.0
for q in old_satilacaklar:
    myq=5.5/q
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    myq=math.ceil(myq * carpim) / carpim
    myqs+=myq
ilkbakiye=len(alinacaklar)*5.5 + (myqs*close)
print("gerekli toplam usdt:", ilkbakiye)
print("Gridler arası yüdelik değişim: ", geometric_percentage)

baslansinmi=input("başlansın mı? (evet/hayır): ")
if baslansinmi.lower()=="evet":
    print("başlanıyor")
else:
    print("tekrar baştan...")
    girdiler()








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

def place_market_buy_order(symbol, quantity):
    """
    Binance API kullanarak bir market alım emri oluşturur.
    
    Args:
        symbol (str): İşlem yapılacak çift (ör. "ONEUSDT").
        quantity (float): Alınacak miktar (ör. 500 ONE).
    
    Returns:
        dict: Emir bilgilerini içeren sözlük.
    """
    global client  # Binance API istemcisini global olarak kullanıyoruz

    try:
        # Market alım emri oluştur
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=format(quantity, '.8f')  # Binance 8 ondalık hane ister
        )
        print("Market alım emri başarıyla oluşturuldu:", order)
        return order
    except Exception as e:
        print("Hata oluştu:", e)
        return None

'''



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

'''

def progress_bar(iterable, desc="Processing"):
    """
    Herhangi bir for döngüsüne progress bar ekler.
    
    Args:
        iterable (iterable): Döngü yapılacak iterable (ör. range, list).
        desc (str): Progress bar açıklaması.
    
    Returns:
        iterable: tqdm ile sarılmış iterable.
    """
    return tqdm(iterable, desc=desc)

# Örnek kullanım
for i in progress_bar(range(100), desc="Yükleniyor"):
    time.sleep(0.05)  # İşlem simülasyonu

'''





def ilkgiris():
    global levels
    global current_price
    global minmiktarondalik
    alinacaklar, satilacaklar = split_levels(levels, current_price)
    new_alinacaklar=alinacaklar[:]
    new_satilacaklar=satilacaklar[:]
    if new_alinacaklar:
        for orderprice in new_alinacaklar:
            #place_buy_order(symbol, orderprice, 10/orderprice)
            print("aşağıya al emri konuldu" , orderprice)
    
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    alinacakcoin=math.ceil(0.00000000000001 * carpim) / carpim
    if new_satilacaklar:
        for orderprice in new_satilacaklar:
            quantity=5.5/orderprice
            quantity=math.ceil(quantity * carpim) / carpim
            alinacakcoin= alinacakcoin+quantity
            #place_sell_order(symbol, orderprice, 10/orderprice)
            print("yukarıya sat emri konuldu ",orderprice, quantity)
    alinacakcoin=math.ceil(alinacakcoin * carpim) / carpim
    #place_market_buy_order(symbol, alinacakcoin)
    print("şu kadar başlangıç için coin alındı: ",alinacakcoin)
    


ilkgiris()
gridprofit=0.0000001
#############

while False:
    random_number = round(generate_random_number(0.04, 0.06),5)
    alemirleri, satemirleri, current_price = get_binance_orders(symbol)
    alinacaklar, satilacaklar = split_levels(levels, current_price)
    new_alinacaklar=alinacaklar[:]
    new_satilacaklar=satilacaklar[:]

    fazlalikalinacaklar = find_excess_items(alemirleri, new_alinacaklar)
    fazlaliksatilacaklar= find_excess_items(satemirleri, new_satilacaklar)

    print(current_price)
    if fazlalikalinacaklar:
        print("alınacaklar: ", fazlalikalinacaklar)
        gridprofit+=len(fazlalikalinacaklar)*(geometric_percentage-comission)*0.01
        for orderprice in fazlalikalinacaklar:
            #place_buy_order(symbol, orderprice, 10/orderprice)
            #print("aşağıya al emri konuldu" , orderprice)
            continue
    if fazlaliksatilacaklar:
        print("satılacaklar: ", fazlaliksatilacaklar)
        for orderprice in fazlaliksatilacaklar:
            #place_sell_order(symbol, orderprice, 10/orderprice)
            #print("yukarıya sat emri konuldu ",orderprice)
            continue
    #old_alinacaklar=new_alinacaklar[:]
    #old_satilacaklar=new_satilacaklar[:]
    print("Gridden elde edilen realized USDT: ",round(gridprofit,2))
    time.sleep(10)



########################## backtest



def process_close_values(file_path):
    global old_satilacaklar
    global old_alinacaklar
    global gridprofit

    """
    Verilen CSV dosyasındaki 'close' sütunundaki her bir değeri işlemeye olanak tanır.
    
    Args:
        file_path (str): CSV dosyasının yolu.
        
    Returns:
        None
    """
    try:
        # CSV dosyasını oku
        data = pd.read_csv(file_path)
        
        # 'close' sütununu kontrol et
        if 'close' in data.columns:
            # tqdm kullanarak ilerleme çubuğu ekle
            sonkapanis=0
            satimsayisi=0
            for index, value in tqdm(enumerate(data['close']), total=len(data['close']), desc="Processing close values"):
                # İşleme yap: burada örnek olarak değeri yazdırıyoruz
                #print(f"Index: {index}, Close Value: {value}")
                # Burada istediğiniz işlemleri yapabilirsiniz
                alinacaklar, satilacaklar = split_levels(levels, value)
                new_alinacaklar=alinacaklar[:]
                new_satilacaklar=satilacaklar[:]
                fazlalikalinacaklar = find_excess_items(old_alinacaklar, new_alinacaklar)
                fazlaliksatilacaklar= find_excess_items(old_satilacaklar, new_satilacaklar)
                old_alinacaklar=new_alinacaklar[:]
                old_satilacaklar=new_satilacaklar[:]

                if fazlalikalinacaklar:
                    #print("alınacaklar: ", fazlalikalinacaklar)
                    gridprofit+= value*(5.5/value)*(geometric_percentage-comission)*0.01*len(fazlalikalinacaklar)#len(fazlalikalinacaklar)*(geometric_percentage-comission)*0.01*5.5*(5.5/value)
                    satimsayisi+=len(fazlalikalinacaklar)
                    for orderprice in fazlalikalinacaklar:
                        #place_buy_order(symbol, orderprice, 10/orderprice)
                        #print("aşağıya al emri konuldu" , orderprice)
                        continue
                if fazlaliksatilacaklar:
                    #print("satılacaklar: ", fazlaliksatilacaklar)
                    for orderprice in fazlaliksatilacaklar:
                        #place_sell_order(symbol, orderprice, 10/orderprice)
                        #print("yukarıya sat emri konuldu ",orderprice)
                        continue
                sonkapanis=value
                #old_alinacaklar=new_alinacaklar[:]
                #old_satilacaklar=new_satilacaklar[:]
            myqs=0.0
            for q in old_satilacaklar:
                myq=5.5/q
                carpim=1
                for i in range(minmiktarondalik):
                    carpim=carpim*10
                myq=math.ceil(myq * carpim) / carpim
                myqs+=myq
            print("myqs",myqs)
            suankibakiye=sonkapanis*myqs + len(old_alinacaklar)*5.5
            kazancorani=(suankibakiye+gridprofit)/(ilkbakiye)
            print("Başlangıç bakiyesi: ", ilkbakiye)
            print("Gridden elde edilen realized USDT: ",round(gridprofit,2))
            print("Gridden yüzde kazanç: ((Grid kazancı / ilk bakiye)*100)  : %",round((gridprofit/ilkbakiye),2)*100)
            print("Şuanki gridden gelen hariç bakiye: ", suankibakiye)
            print("Şuanki grid dahil bakiye / ilk bakiye= ",round(kazancorani,2))
            print("Tamamlanmış işlem sayısı: ",satimsayisi)

        else:
            raise ValueError("'close' sütunu bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")

# Örnek kullanım
#file_path = 'BTCUSDT_1m.csv'  # CSV dosyasının yolu
if True:
    process_close_values(file_path)

