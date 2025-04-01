#grid bot backtest by recep yeni recepyeni@gmail.com
#import numpy as np
import time
import random
from binance.client import Client
from binance.enums import * #SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from tqdm import tqdm
from decimal import Decimal
import math
#import pandas as pd
import sys
#import csv
import requests
from datetime import datetime, timedelta, timezone
import os
#from tqdm import tqdm
#import pandas as pd
#import math


api_key = "Your_Api_Key"
api_secret = "Your_Secret_Key"

client=Client(api_key, api_secret)



botmubacktestmi=int(input("Bot için 1 yazın, backtest için 2 yazın: "))
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
data_first_close = 0.032
veriinterval = "1m" #input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
veri_days_back = 3 # int(input("Enter the number of days back to fetch (e.g. 3): "))
data=[]
girilenilkbakiye=0
mymyq=0.0
carpim=1
old_alinacaklar=[]
old_satilacaklar=[]
start_date="2024-01-01"
end_date="2024-12-17"


'''
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
            print("first close: ",first_close)
            return first_close
        else:
            raise ValueError("'close' sütunu bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")
        return None

# Örnek kullanım
file_path = 'LTCUSDT_1m.csv'  # CSV dosyasının yolu
close = get_first_close(file_path)
if close is not None:
    print(f"İlk 'close' fiyatı: {close}")
'''

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
    global data_first_close
    global veriinterval
    global veri_days_back
    global start_date
    global end_date
    global data
    global girilenilkbakiye
    symbol = input("Coin Çiftini Giriniz (Örn: BTCUSDT): ").upper()
    start = float(input("Alt seviyeyi giriniz (Örn: 0.02): "))
    end = float(input("Üst seviyeyi giriniz (Örn: 0.6): "))
    num_levels = int(input("Grid sayısını giriniz (Binance limit=max 200) (Örn: 200): "))
    comission=float(input("Komisyon (Örn: %0.1 (yani binde bir)): %"))
    girilenilkbakiye=int(input("Başlangıç sermayesi kaç USDT olsun (öRN 1000): "))
    veriinterval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    #veri_days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))
    start_date=input("Botun çalışma başlangıç tarihini yıl tire ay tire gün şeklinde yazınız (Örn. 2024-01-17)")
    end_date=input("Botun çalışma bitiş tarihini yıl tire ay tire gün şeklinde yazınız (Örn. 2024-12-27)")
    data=vericekis(veriinterval,start_date,end_date)
    data_first_close=float(data[0][4])

    minmiktarondalik,myticksize,precision_info=get_precision(symbol)
    levels, geometric_percentage = geometric_division(start, end, num_levels)


def calisanbotgirdiler():
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
    global data_first_close
    global veriinterval
    global veri_days_back
    global start_date
    global end_date
    global data
    global girilenilkbakiye
    global mymyq
    global carpim
    symbol = input("Coin Çiftini Giriniz (Örn: BTCUSDT): ").upper()
    start = float(input("Alt seviyeyi giriniz (Örn: 0.02): "))
    end = float(input("Üst seviyeyi giriniz (Örn: 0.6): "))
    num_levels = int(input("Grid sayısını giriniz (Örn: 200): "))
    comission=float(input("Komisyon (Örn: %0.1 (yani binde bir)): %"))
    
    #veriinterval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    #veri_days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))
    #data=vericekis(veriinterval,veri_days_back)
    #data_first_close=float(data[0][4])

    minmiktarondalik,myticksize,precision_info=get_precision(symbol)
    levels, geometric_percentage = geometric_division(start, end, num_levels)
    mymyq=5.5/start
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    mymyq=math.ceil(mymyq * carpim) / carpim #hep aynı quantity de alınacak.
    minsermaye=0.0
    pricedata=get_coin_data(symbol) #price,high,low
    alinacaklar, satilacaklar = split_levels(levels, pricedata[0], pricedata[1],pricedata[2])
    asagidakialinacaklarusdt=0.0
    for level in alinacaklar:
        asagidakialinacaklarusdt+=level*mymyq
    yukaridakisatilacaklarusdt=mymyq*pricedata[0]*len(satilacaklar)

    print("grid aralıkları: %",geometric_percentage)
    print("Gdir sayısı: ",num_levels)
    print("Min gerekli sermaye: ",(asagidakialinacaklarusdt+yukaridakisatilacaklarusdt))
    girilenilkbakiye=int(input("Başlangıç sermayesi kaç USDT olsun (Örn. 1000): "))


def get_coin_price(symbol):
    """
    Belirtilen coin çiftinin fiyatını döndürür.
    :param symbol: Coin çifti (örn: 'ONEUSDT')
    :return: Fiyat (float) veya None (hata durumunda)
    """
    url = f"https://api.binance.com/api/v3/ticker/price"
    params = {'symbol': symbol.upper()}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Hata varsa tetikler
        price = float(response.json()['price'])
        return price
    except Exception as e:
        print(f"Hata: {e}")
        return None


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
    """
    Belirli bir aralığı geometrik olarak bölerek seviyeleri döndürür.

    Args:
        start (float): Başlangıç değeri (aralığın alt sınırı).
        end (float): Bitiş değeri (aralığın üst sınırı).
        num_levels (int): Bölünmek istenen geometrik seviye sayısı.

    Returns:
        list: Geometrik seviyelerin bir listesi.
        float: Geometrik yüzde.
    """
    if num_levels <= 1:
        raise ValueError("Number of levels must be greater than 1.")
    
    levels = []
    ratio = (end / start) ** (1 / (num_levels - 1))
    current = start
    for _ in range(num_levels):
        levels.append(round(current, 8))  # İstenirse hassasiyet artırılabilir.
        current *= ratio

    geometric_percentage = ((levels[1] - levels[0]) / levels[0]) * 100 if len(levels) > 1 else 0
    return levels, round(geometric_percentage, 2)

'''
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
'''

################ Veri çekiş

def fetch_binance_klines(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": int(start_time.timestamp() * 1000),
        "endTime": int(end_time.timestamp() * 1000),
        "limit": 1000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data from Binance: {response.status_code} {response.text}")





# Function to collect data between two dates
def collect_data(symbol, interval, start_date, end_date):
    start_time = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)  # UTC-aware
    end_time = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)  # UTC-aware

    if start_time >= end_time:
        raise ValueError("Start date must be earlier than end date.")

    print(f"Fetching data for {symbol} with interval {interval} from {start_date} to {end_date}...")
    all_data = []
    current_start_time = start_time

    total_steps = (end_time - start_time).days + 1
    with tqdm(total=total_steps, desc=f"Processing {symbol} - {interval}") as pbar:
        while current_start_time < end_time:
            current_end_time = min(current_start_time + timedelta(days=1), end_time)
            try:
                klines = fetch_binance_klines(symbol, interval, current_start_time, current_end_time)
                for kline in klines:
                    timestamp = datetime.fromtimestamp(kline[0] / 1000, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    open_price = kline[1]
                    high_price = kline[2]
                    low_price = kline[3]
                    close_price = kline[4]
                    volume = kline[5]
                    all_data.append([timestamp, open_price, high_price, low_price, close_price, volume])
                current_start_time = datetime.fromtimestamp(klines[-1][6] / 1000, tz=timezone.utc)
            except Exception as e:
                print(f"Error fetching data: {e}")
                break

            pbar.update(1)

    return all_data

# Example usage
# data = collect_data("BTCUSDT", "1h", "2024-01-01", "2024-12-17")



def collect_data_eski(symbol, interval, days_back): #iptal edildi
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)  # UTC-aware
    start_time = (end_time - timedelta(days=days_back)).replace(tzinfo=timezone.utc)  # UTC-aware

    print(f"Fetching data for {symbol} with interval {interval}...")
    all_data = []
    current_start_time = start_time

    total_steps = (end_time - start_time).days + 1
    with tqdm(total=total_steps, desc=f"Processing {symbol} - {interval}") as pbar:
        while current_start_time < end_time:
            current_end_time = min(current_start_time + timedelta(days=1), end_time)
            try:
                klines = fetch_binance_klines(symbol, interval, current_start_time, current_end_time)
                for kline in klines:
                    timestamp = datetime.fromtimestamp(kline[0] / 1000, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    open_price = kline[1]
                    high_price = kline[2]
                    low_price = kline[3]
                    close_price = kline[4]
                    volume = kline[5]
                    all_data.append([timestamp, open_price, high_price, low_price, close_price, volume])
                current_start_time = datetime.fromtimestamp(klines[-1][6] / 1000, tz=timezone.utc)
            except Exception as e:
                print(f"Error fetching data: {e}")
                break

            pbar.update(1)

    return all_data


'''
def collect_data(symbol, interval, days_back):
    """
    Binance API'den geçmiş fiyat verilerini toplar.

    Args:
        symbol (str): Coin çifti.
        interval (str): Zaman aralığı (örn. "1m", "5m", "1h", "1d").
        days_back (int): Kaç günlük veri çekileceği.

    Returns:
        list: Veriler [timestamp, open, high, low, close, volume] formatında.
    """
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    start_time = end_time - timedelta(days=days_back)

    print(f"Fetching data for {symbol} with interval {interval}...")
    all_data = []
    current_start_time = start_time

    while current_start_time < end_time:
        current_end_time = min(current_start_time + timedelta(days=1), end_time)
        try:
            klines = fetch_binance_klines(symbol, interval, current_start_time, current_end_time)
            for kline in klines:
                timestamp = datetime.fromtimestamp(kline[0] / 1000, tz=timezone.utc).isoformat()
                open_price, high_price, low_price, close_price, volume = map(float, kline[1:6])
                all_data.append([timestamp, open_price, high_price, low_price, close_price, volume])
            current_start_time = datetime.fromtimestamp(klines[-1][6] / 1000, tz=timezone.utc)
        except Exception as e:
            print(f"Error fetching data: {e}")
            break

    return all_data
'''

def vericekis(veriinterval, start_date,end_date):
    # Kullanıcıdan input alma
    #symbol = input("Enter the coin pair (e.g., BTCUSDT): ").strip().upper()
    global symbol
    

    #interval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    #days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))

    # Veri toplama
    data = collect_data(symbol, veriinterval, start_date,end_date)

    return data
###############


# Örnek kullanım


alinacaklar=[]
satilacaklar=[]
oncekialinacaklar=[]
oncekisatilacaklar=[]
oncekialinacaklevelsonprice=1000000
oncekisatilacaklevelilkprice=1000000
def split_levels(levels, myclose,high=None,low=None):
    if True:#close>start and close<end:
        global oncekialinacaklevelsonprice
        global oncekisatilacaklevelilkprice
        global oncekialinacaklar
        global oncekisatilacaklar
        global alinacaklar
        global satilacaklar
        """
        Levels listesini ikiye böler: close'dan düşük olanlar ve yüksek olanlar.
        
        Args:
            levels (list): Geometrik seviyelerin bir listesi.
            close (float): Close değeri, seviyelere göre listeyi böler.
        
        Returns:
            tuple: (alinacaklar, satilacaklar) listeleri.
        """
        # En yakın elemanı bul ve sil
        
        
        if not levels:
            print("Hata: 'levels' listesi boş!")
            sys.exit()
            return [], []

        # Close değerine göre böl
        if low is not None and high is not None:
            if high<levels[0]:
                alinacaklar=[]
                satilacaklar=levels[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                return alinacaklar, satilacaklar
            elif low>levels[-1]:
                alinacaklar=levels[:]
                satilacaklar=[]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                return alinacaklar, satilacaklar
        else:
            if myclose<levels[0]:
                alinacaklar=[]
                satilacaklar=levels[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                return alinacaklar, satilacaklar
            elif myclose>levels[-1]:
                alinacaklar=levels[:]
                satilacaklar=[]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                return alinacaklar, satilacaklar

        
        #print(satilacaklar)
        #print(alinacaklar)
        if oncekisatilacaklevelilkprice==1000000:
            closest_level = min(levels, key=lambda x: abs(x - myclose))
            gecicilevels=levels[:]
            gecicilevels.remove(closest_level)
            satilacaklar = [level for level in gecicilevels if level > myclose]
            alinacaklar = [level for level in gecicilevels if level < myclose]
            oncekisatilacaklar = satilacaklar[:]
            oncekialinacaklar = alinacaklar[:]
            oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
            oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]

        
            
            
    
        if low is not None and high is not None:
    
            if low> oncekialinacaklevelsonprice and high<oncekisatilacaklevelilkprice:
                return oncekialinacaklar, oncekisatilacaklar
            elif low<oncekialinacaklevelsonprice:
                closest_level = min(levels, key=lambda x: abs(x - low))
                gecicilevels=levels[:]
                gecicilevels.remove(closest_level)
                #gecicilevels = [level for level in gecicilevels if not (low <= level <= high)]

                satilacaklar = [level for level in gecicilevels if level > low]
                alinacaklar = [level for level in gecicilevels if level < low]
                oncekisatilacaklar=satilacaklar[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                oncekialinacaklar = alinacaklar[:]
                return alinacaklar, satilacaklar
            elif high>oncekisatilacaklevelilkprice:
                closest_level = min(levels, key=lambda x: abs(x - high))
                gecicilevels=levels[:]
                gecicilevels.remove(closest_level)
                #gecicilevels = [level for level in levels if not (low <= level <= high)]

                satilacaklar = [level for level in gecicilevels if level > high]
                alinacaklar = [level for level in gecicilevels if level < high]
                oncekisatilacaklar=satilacaklar[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                oncekialinacaklar = alinacaklar[:]
                return alinacaklar, satilacaklar
            else:
                closest_level = min(levels, key=lambda x: abs(x - myclose))
                gecicilevels=levels[:]
                gecicilevels.remove(closest_level)
                satilacaklar = [level for level in gecicilevels if level > myclose]
                alinacaklar = [level for level in gecicilevels if level < myclose]
                oncekisatilacaklar = satilacaklar[:]
                oncekialinacaklar = alinacaklar[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                
                return alinacaklar, satilacaklar
        else:
            if myclose> oncekialinacaklevelsonprice and myclose<oncekisatilacaklevelilkprice:
                return oncekialinacaklar, oncekisatilacaklar
            else:
                closest_level = min(levels, key=lambda x: abs(x - myclose))
                gecicilevels=levels[:]
                gecicilevels.remove(closest_level)
                satilacaklar = [level for level in gecicilevels if level > myclose]
                alinacaklar = [level for level in gecicilevels if level < myclose]
                oncekisatilacaklar = satilacaklar[:]
                oncekialinacaklar = alinacaklar[:]
                oncekisatilacaklevelilkprice=satilacaklar[0] if satilacaklar else levels[-1]
                oncekialinacaklevelsonprice=alinacaklar[-1] if alinacaklar else levels[0]
                return alinacaklar, satilacaklar

# Örnek kullanım


#print(levels)


"""

myqsyukari=0.0 #iptal edildi. artık her yere sabit q
for q in old_satilacaklar:
    myq=5.5/q
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    myq=math.ceil(myq * carpim) / carpim
    myqsyukari+=myq





myassetsasagi=0.0
for q in old_alinacaklar: #iptal
    mya=q * mymyq
    carpim=1
    for i in range(myticksize):
        carpim=carpim*10
    mya=math.ceil(mya * carpim) / carpim
    myassetsasagi+=myassetsasagi
myassetsasagi=5.5*len(alinacaklar)#iptal
"""
def ilkbakiyehesapla():
    q1=5.5/start
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    q1=math.ceil(q1 * carpim) / carpim # hep aynı quantity de alınacak.
    gereklialtusdt=0.0
    
    for level in old_alinacaklar:
        gereklialtusdt+=math.ceil((level*q1)*carpim)/carpim
    gerekliustusdt=(math.ceil((current_price*q1)*carpim)/carpim)*len(old_satilacaklar)
    return (gereklialtusdt+gerekliustusdt)

def sonbakiyehesapla(sonclose,sonalinacaklar, sonsatilacaklar):
    q1=5.5/start
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    q1=math.ceil(q1 * carpim) / carpim # hep aynı quantity de alınacak.
    gereklialtusdt=0.0
    
    for level in sonalinacaklar:
        gereklialtusdt+=math.ceil((level*q1)*carpim)/carpim
    gerekliustusdt=(math.ceil((sonclose*q1)*carpim)/carpim)*len(sonsatilacaklar)
    return (gereklialtusdt+gerekliustusdt)




while False:
    baslansinmi=input("başlansın mı? (evet/hayır): ")
    if baslansinmi.lower()=="evet":
        print("başlanıyor")
        break
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
#close = 0.05



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
#start = 0.02
#end = 0.6

#random_number = round(generate_random_number(start, end),5)
#print("Rastgele Sayı:", random_number)


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





###########



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




##################


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


import requests

def get_coin_data(symbol):
    """
    Coin çiftinin fiyat, high ve low değerlerini döndürür.
    :param symbol: Coin çifti (örn: 'ONEUSDT')
    :return: Liste [price, high, low] veya None (hata durumunda)
    """
    url = f"https://api.binance.com/api/v3/ticker/24hr"
    params = {'symbol': symbol.upper()}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Hata varsa tetikler
        data = response.json()
        price = float(data['lastPrice'])
        high = float(data['highPrice'])
        low = float(data['lowPrice'])
        return [price, high, low]
    except Exception as e:
        print(f"Hata: {e}")
        return None






def ilkgiris():
    global levels
    global current_price
    global minmiktarondalik
    alinacaklar, satilacaklar = split_levels(levels, float(data[0][4]))
    new_alinacaklar=alinacaklar[:]
    new_satilacaklar=satilacaklar[:]
    if new_alinacaklar:
        for orderprice in new_alinacaklar:
            #place_buy_order(symbol, orderprice, mymyq)
            print("aşağıya al emri konuldu" , orderprice)
    
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    alinacakcoin=math.ceil(0.00000000000001 * carpim) / carpim
    if new_satilacaklar:
        for orderprice in new_satilacaklar:
            quantity=mymyq
            #quantity=math.ceil(quantity * carpim) / carpim
            alinacakcoin= alinacakcoin+quantity
            #place_sell_order(symbol, orderprice, mymyq)
            print("yukarıya sat emri konuldu ",orderprice, quantity)
    alinacakcoin=math.ceil(alinacakcoin * carpim) / carpim
    #place_market_buy_order(symbol, alinacakcoin)
    print("şu kadar başlangıç için coin alındı: ",alinacakcoin)
    



def create_and_write_txt(file_name, content):
    """
    Belirtilen isimle bir txt dosyası oluşturur ve içine belirtilen içeriği yazar.

    Args:
        file_name (str): Dosya adı (uzantı .txt ile bitmeli).
        content (str): Dosyaya yazılacak içerik.
    """
    if not file_name.endswith('.txt'):
        file_name += '.txt'
    
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"'{file_name}' dosyası başarıyla oluşturuldu ve içerik yazıldı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")


def read_api_key(dosya):
    try:
        with open(dosya, "r") as file: #"akey.txt"
            return file.read().strip()  # Dosyadaki metni okuyup döner
    except FileNotFoundError:
        return None  # Dosya yoksa None döner

# Kullanımı
#api_key = read_api_key()
#if api_key:
#    print(f"API Anahtarı: {api_key}")
#else:
#    print("api_key.txt dosyası bulunamadı veya okunamadı.")

def check_api_key_file():
    # Çalışma dizinindeki api_key.txt dosyasını kontrol eder
    myapi=os.path.isfile("a.txt")
    mysecret=os.path.isfile("s.txt")
    return (myapi and mysecret)

# Kullanımı
#if check_api_key_file():
#    print("api_key.txt dosyası bulundu.")
#else:
#    print("api_key.txt dosyası bulunamadı.")

def get_current_datetime_text():
    """
    Şimdiki zamanı yıl, ay, gün, saat, dakika ve saniye olarak metin şeklinde döndürür.

    Returns:
        str: Yıl, ay, gün, saat, dakika ve saniyeyi içeren zaman bilgisi.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S")

# Kullanımı
#current_time_text = get_current_datetime_text()
#print(current_time_text)

gridprofit=0.0000001
#############

def toplam_kar_hesapla(son_fiyat, yuzde_artis, komisyon_orani, lot_sayisi):
    """
    Toplam karı hesaplayan fonksiyon.

    Parametreler:
    - son_fiyat: İşlemin bitiş fiyatı.
    - yuzde_artis: Başlangıç fiyatından itibaren yüzde kaç artışla son fiyata ulaşıldı (örn: 1 için %1).
    - komisyon_orani: Komisyon oranı (örn: 0.003 için %0.3).
    - lot_sayisi: İşlem yapılan toplam lot sayısı.

    Return:
    - toplam_kar: İşlemden elde edilen toplam kar.
    """
    # Başlangıç fiyatını hesapla
    baslangic_fiyati = son_fiyat / (1 + yuzde_artis)

    # Birim başına karı hesapla
    birim_kar = (son_fiyat - baslangic_fiyati) - (son_fiyat * komisyon_orani)

    # Toplam karı hesapla
    toplam_kar = birim_kar * lot_sayisi

    return toplam_kar

#son_fiyat = 123
#yuzde_artis = 0.01  # %1 artış
#komisyon_orani = 0.003  # %0.3 komisyon
#lot_sayisi = 14

#kar = toplam_kar_hesapla(son_fiyat, yuzde_artis, komisyon_orani, lot_sayisi)
#print(f"Toplam kar: {kar:.2f}")



def ilkveonbakiyehesapla():
    global data
    global levels
    mymyilkprice=float(data[0][4])
    mymyilkhigh=float(data[0][2])
    mymyilklow=float(data[0][3])
    mymysonprice=float(data[-1][4])
    mymysonhigh=float(data[-1][2])
    mymysonlow=float(data[-1][3])
    levels, geometric_percentage = geometric_division(start, end, num_levels)
    mymyilkbakiye=0.0
    suankibakiye=0.0
    try:
        ilk_alinacaklar, ilk_satilacaklar = split_levels(levels, mymyilkprice, mymyilkhigh, mymyilklow)
        son_alinacaklar, son_satilacaklar = split_levels(levels, mymysonprice, mymysonhigh, mymysonlow)
    except:
        print("sorun çıktı1")
    try:
        mymyilkbakiye=sonbakiyehesapla(mymyilkprice,ilk_alinacaklar,ilk_satilacaklar)
        suankibakiye=sonbakiyehesapla(mymysonprice,son_alinacaklar,son_satilacaklar)
    except:
        print("sorun çıktı2")
    return mymyilkbakiye,suankibakiye


from datetime import datetime

def calculate_days_between(start_date, end_date):
    """
    Calculates the number of days between two dates.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        int: The number of days between the two dates.
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            raise ValueError("Start date must be earlier than end date.")

        difference = (end - start).days
        return difference
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Example usage:
#days_between = calculate_days_between("2024-01-17", "2024-12-27")
#print(f"Number of days between: {days_between}")


def process_close_values(data):
    global old_satilacaklar
    global old_alinacaklar
    global gridprofit
    global veri_days_back
    global levels

    """
    Verilen veri listesindeki 'close', 'high', ve 'low' sütunlarındaki değerleri işlemeye olanak tanır.
    
    Args:
        data (list): Binance API'den alınan veri.
        
    Returns:
        None
    """
    try:
        # Gerekli sütunların varlığını kontrol et
        if len(data) > 0:
            sonkapanis = 0
            satimsayisi = 0
            for row in tqdm(data, desc="Processing close values"):
                close_value = float(row[4])
                high_value = float(row[2])
                low_value = float(row[3])

                if close_value > start and close_value < end:
                    try:
                        new_alinacaklar, new_satilacaklar = split_levels(levels, close_value, high_value, low_value)
                    except Exception as e:
                        print(f"Hata: {e} burada out list index diyor de mi?")
                        new_alinacaklar = old_alinacaklar[:]
                        new_satilacaklar = old_satilacaklar[:]
                        continue

                    fazlalikalinacaklar = find_excess_items(old_alinacaklar, new_alinacaklar)
                    fazlaliksatilacaklar = find_excess_items(old_satilacaklar, new_satilacaklar)
                    old_alinacaklar = new_alinacaklar[:]
                    old_satilacaklar = new_satilacaklar[:]

                    if fazlalikalinacaklar:
                        satimsayisi += len(fazlalikalinacaklar)
                        for price in fazlalikalinacaklar:
                            gridprofit+=toplam_kar_hesapla(price,(geometric_percentage*0.01),(comission*0.01),mymyq)
                        """
                        if close_value * mymyq > 5.5:
                            gridprofit += close_value * mymyq * (geometric_percentage - comission) * 0.01 * len(fazlalikalinacaklar)
                        else:
                            gridprofit += 5.5 * (geometric_percentage - comission) * 0.01 * len(fazlalikalinacaklar)
                        satimsayisi += len(fazlalikalinacaklar)
                        for orderprice in fazlalikalinacaklar:
                            # place_buy_order(symbol, orderprice, mymyq)
                            continue
                        """
                    #if fazlaliksatilacaklar:
                    #    for orderprice in fazlaliksatilacaklar:
                            # place_sell_order(symbol, orderprice, mymyq)
                    #        continue

                sonkapanis = close_value

            # Sonuç hesaplamaları
            myqs = sum(math.ceil(5.5 / q * (10**minmiktarondalik)) / (10**minmiktarondalik) for q in old_satilacaklar)
            mysatilacakq = mymyq * len(old_satilacaklar)
            alinacaklartoplamusdt = sum(alinacakusdt * mymyq for alinacakusdt in old_alinacaklar)
            satilacaklartoplamusdt = sonkapanis * mysatilacakq 
            #suankibakiye = satilacaklartoplamusdt + alinacaklartoplamusdt
            yavilkbakiyeiste, yavsonbakiyeiste=ilkveonbakiyehesapla()
            
            kazancorani = (yavsonbakiyeiste + gridprofit) / yavilkbakiyeiste
            girilenboluminbakiye=round((girilenilkbakiye/yavilkbakiyeiste),2)
            
            istatistik=f"""
            Sembol: {symbol}
            Alt sınır: {start} USDT
            Üst sınır: {end} USDT
            Grid Sayısı: {num_levels}
            Komisyon: %{comission}
            Bot başlangıç tarihi: {start_date}
            Bot bitiş tarihi: {end_date}
            Kaç gündür bot çalışıyor: {calculate_days_between(start_date,end_date)} gün
            Gridler arası yüzde: %{geometric_percentage}
            Binance'ta açmak için gerekli min. bakiye: {yavilkbakiyeiste} USDT
            Başlangıç bakiyesi: {girilenilkbakiye} USDT
            Tamamlanmış işlem sayısı: {satimsayisi}
            Gridden elde edilen realized USDT: {round(gridprofit*girilenboluminbakiye, 2)} USDT
            Gridden yüzde kazanç ((Grid kazancı bölü ilk bakiye) * 100): %{round((round((gridprofit / yavilkbakiyeiste), 2) * 100),2)}
            Şuanki gridden gelen hariç bakiye: {round(yavsonbakiyeiste*girilenboluminbakiye , 2)} USDT
            Şuanki grid dahil bakiye: {round((yavsonbakiyeiste + gridprofit) * girilenboluminbakiye , 2)} USDT
            Şuanki grid dahil bakiye bölü ilk bakiye: {round(kazancorani, 2)} X (yani toplam %{round(100*(round(kazancorani, 2)-1),2)} ekstra gelir gelmiş.)
            Bot başlarkenki coin fiyatı: {data[0][4]} USDT
            Bot bitişindeki coin fiyatı: {data[-1][4]} USDT
            """
            print(istatistik)
            '''
            print(symbol)
            print("Alt sınır: ", start)
            print("Üst sınır: ", end)
            print("Grid sayısı: ", num_levels)
            print("Komisyon: %", comission)
            print("Kaç gündür bot çalışıyor: ",veri_days_back)
            
            print("Gridler arası yüzde: %", geometric_percentage)
            print("Başlangıç bakiyesi: ", girilenilkbakiye)
            print("Tamamlanmış işlem sayısı: ", satimsayisi)
            print("Gridden elde edilen realized USDT: ", round(gridprofit*girilenboluminbakiye, 2))
            print("Gridden yüzde kazanç: ((Grid kazancı / ilk bakiye)*100)  : %", round((gridprofit / yavilkbakiyeiste), 2) * 100)
            print("Şuanki gridden gelen hariç bakiye: ", round(yavsonbakiyeiste*girilenboluminbakiye , 2))
            print("Şuanki grid dahil bakiye / ilk bakiye= ", round(kazancorani, 2))
            print("Coin ilk fiyatı: ",data_first_close)
            print("Coin son fiyatı: ",data[-1][4])
            '''
            
            file_name = f"{symbol}-{calculate_days_between(start_date,end_date)}gun-gridKarYuzde{round((gridprofit / yavilkbakiyeiste), 2) * 100}-bakiyeYuzde{round(kazancorani, 2)}-aralikYuzde{geometric_percentage}-{get_current_datetime_text()}"
            create_and_write_txt(file_name, istatistik)

        else:
            raise ValueError("Data is empty.")
    except Exception as e:
        print(f"Hata: {e}")

def mygridbot():
    global old_alinacaklar
    global old_satilacaklar
    global client
    apisecretvarmi=check_api_key_file()
    if apisecretvarmi==True:
        myapi=read_api_key("a.txt")
        mysecret=read_api_key("s.txt")
        client=Client(myapi, mysecret)
    else:
        myapi=input("Binance Api Key giriniz: ")
        mysecret=input("Binance Secret Key giriniz: ")
        create_and_write_txt("a.txt",myapi)
        create_and_write_txt("s.txt",mysecret)
        client=Client(myapi, mysecret)

    ilkmi="evet"
    calisanbotgirdiler()
    gridprofit=0.0
    while True:
        pricedata=get_coin_data(symbol) #price,high,low
        random_number = round(generate_random_number(0.04, 0.06),5)
        alemirleri, satemirleri, current_price = get_binance_orders(symbol)
        alinacaklar, satilacaklar = split_levels(levels, pricedata[0], pricedata[1],pricedata[2])
        new_alinacaklar=alinacaklar[:]
        new_satilacaklar=satilacaklar[:]
        
        fazlalikalinacaklar = find_excess_items(alemirleri, new_alinacaklar)
        fazlaliksatilacaklar= find_excess_items(satemirleri, new_satilacaklar)

        #print(current_price)
        if fazlalikalinacaklar:
            print("alınacaklar: ", fazlalikalinacaklar)
            
                
            #gridprofit+=len(fazlalikalinacaklar)*(geometric_percentage-comission)*0.01*mymyq*current_price
            for orderprice in fazlalikalinacaklar:
                gridprofit+=toplam_kar_hesapla(orderprice,(geometric_percentage*0.01),(comission*0.01),mymyq)
                place_buy_order(symbol, orderprice, mymyq)
                print("aşağıya al emri konuldu" , orderprice)
                continue
        if fazlaliksatilacaklar:
            if ilkmi=="evet":
                
                place_market_buy_order(symbol, (mymyq*len(fazlaliksatilacaklar)))
                print("ilk alınacaklar alındı")
                ilkmi="hayır"
                    
            print("satılacaklar: ", fazlaliksatilacaklar)
            for orderprice in fazlaliksatilacaklar:
                place_sell_order(symbol, orderprice, mymyq)
                print("yukarıya sat emri konuldu ",orderprice)
                
        old_alinacaklar=new_alinacaklar[:]
        old_satilacaklar=new_satilacaklar[:]
        print("Gridden elde edilen realized USDT: ",round(gridprofit,2))
        time.sleep(10)


def mybacktest():
    global symbol
    global mymyq
    global carpim
    global alinacaklar
    global satilacaklar
    global old_alinacaklar
    global old_satilacaklar
    global ilkbakiye
    global new_alinacaklar
    global new_satilacaklar
    global fazlalikalinacaklar 
    global fazlaliksatilacaklar
    #global alemirleri
    #global satemirleri
    global current_price
    print("Backtest çalışmaya başladı")
    girdiler()
    current_price=get_coin_price(symbol)
    alinacaklar, satilacaklar = split_levels(levels, float(data[0][4]))
    old_alinacaklar=alinacaklar[:]
    old_satilacaklar=satilacaklar[:]
    new_alinacaklar=alinacaklar[:]
    new_satilacaklar=satilacaklar[:]
    #print("Alinacaklar:", alinacaklar)
    #print("Satilacaklar:", satilacaklar)

    print("Precision bilgileri:", minmiktarondalik)
    mymyq=5.5/start
    carpim=1
    for i in range(minmiktarondalik):
        carpim=carpim*10
    mymyq=math.ceil(mymyq * carpim) / carpim #hep aynı quantity de alınacak.
    ilkbakiye, yavsonbakiyeiste=ilkveonbakiyehesapla()
    #ilkbakiye,= ilkbakiyehesapla()   #myassetsasagi + (mymyq*close)*len(satilacaklar)
    print("minimum gerekli toplam usdt:", ilkbakiye)
    print("Gridler arası yüdelik değişim: ", geometric_percentage)
    #new_alinacaklar, new_satilacaklar = split_levels(levels, data_first_close)

    fazlalikalinacaklar = find_excess_items(old_alinacaklar, new_alinacaklar)
    fazlaliksatilacaklar= find_excess_items(old_satilacaklar, new_satilacaklar)
    #print("Fazlalikalinacaklar:", fazlalikalinacaklar)
    #print("Fazlaliksatilacaklar:", fazlaliksatilacaklar)
    #alemirleri, satemirleri, current_price = get_binance_orders(symbol)

    #print("Al Emirleri (alemirleri):", alemirleri)
    #print("Sat Emirleri (satemirleri):", satemirleri)
    ilkgiris()
    process_close_values(data)

if botmubacktestmi==1:
    mygridbot()
elif botmubacktestmi==2:
    mybacktest()
else:
    print("lütfen çecerli bir giriş yapınız.")


"""

### Fonksiyonlar ve Açıklamaları

1. **`girdiler()`**
   - Kullanıcıdan grid bot veya backtest için gerekli verileri (örneğin coin çifti, alt/üst limitler, grid sayısı vb.) alır ve gerekli global değişkenleri hazırlar.

2. **`calisanbotgirdiler()`**
   - Aktif olarak çalışan grid bot için kullanıcıdan gerekli verileri alır, başlangıç ayarlarını yapar ve gerekli hesaplamaları gerçekleştirir.

3. **`get_coin_price(symbol)`**
   - Binance API'sinden belirli bir coin çiftinin güncel fiyatını döndürür.

4. **`count_decimal_places(number)`**
   - Verilen bir sayının ondalık kısmındaki anlamlı basamak sayısını döndürür.

5. **`get_precision(symbol)`**
   - Binance API'sinden belirli bir coin çiftinin miktar ve fiyat hassasiyetini (precision) alır.

6. **`geometric_division(start, end, num_levels)`**
   - Verilen aralığı geometrik olarak böler ve grid seviyelerini oluşturur.

7. **`fetch_binance_klines(symbol, interval, start_time, end_time)`**
   - Binance API'sinden belirli bir zaman aralığındaki geçmiş fiyat verilerini çeker.

8. **`collect_data(symbol, interval, days_back)`**
   - Belirtilen gün sayısı kadar geçmiş fiyat verisini toplar ve işlemeye hazır hale getirir.

9. **`vericekis(veriinterval, veri_days_back)`**
   - Kullanıcı tarafından belirtilen zaman aralığı ve gün sayısına göre veri toplar.

10. **`split_levels(levels, myclose, high=None, low=None)`**
    - Grid seviyelerini belirli bir fiyatın alt ve üst seviyelerine böler ve alınacak/satılacak seviyeleri döndürür.

11. **`ilkbakiyehesapla()`**
    - Grid botun başında gereken minimum bakiyeyi hesaplar.

12. **`sonbakiyehesapla(sonclose, sonalinacaklar, sonsatilacaklar)`**
    - Botun çalışması sonucunda kalan toplam bakiyeyi hesaplar.

13. **`find_excess_items(old_list, new_list)`**
    - Yeni ve eski alınacak/satılacak listelerindeki farkları bulur.

14. **`generate_random_number(start, end)`**
    - Belirtilen bir aralıkta rastgele bir sayı üretir.

15. **`get_binance_orders(symbol)`**
    - Binance API'sinden belirli bir coin çifti için açık alım ve satım emirlerini alır.

16. **`place_sell_order(symbol, price, quantity)`**
    - Binance üzerinde belirtilen fiyatta ve miktarda bir satış limiti emri oluşturur.

17. **`place_market_buy_order(symbol, quantity)`**
    - Binance üzerinde belirtilen miktarda bir market alım emri oluşturur.

18. **`place_buy_order(symbol, price, quantity)`**
    - Binance üzerinde belirtilen fiyatta ve miktarda bir alım limiti emri oluşturur.

19. **`get_coin_data(symbol)`**
    - Coin çiftinin fiyat, en yüksek ve en düşük değerlerini döndürür.

20. **`ilkgiris()`**
    - Grid botun ilk çalıştırılmasında alınacak/satılacak emirleri ve başlangıçtaki gerekli coin miktarını belirler.

21. **`create_and_write_txt(file_name, content)`**
    - Belirtilen isimde bir dosya oluşturur ve verilen içeriği dosyaya yazar.

22. **`read_api_key(dosya)`**
    - API anahtarını bir dosyadan okur ve döndürür.

23. **`check_api_key_file()`**
    - API anahtar dosyalarının mevcut olup olmadığını kontrol eder.

24. **`get_current_datetime_text()`**
    - Şimdiki zamanı yıl, ay, gün, saat, dakika ve saniye formatında metin olarak döndürür.

25. **`ilkveonbakiyehesapla()`**
    - Botun başlangıç ve son bakiyelerini hesaplar.

26. **`process_close_values(data)`**
    - Verilen veri listesi üzerinde grid bot işlemlerini simüle eder ve sonuçları hesaplar.

27. **`mygridbot()`**
    - Binance üzerinde gerçek zamanlı çalışan grid botu başlatır ve döngü içinde çalıştırır.

28. **`mybacktest()`**
    - Belirtilen zaman aralığında geçmiş fiyat verilerini kullanarak grid botun performansını test eder.

"""