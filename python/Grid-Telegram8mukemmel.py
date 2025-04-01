from telethon import TelegramClient, events
import asyncio
import requests
# Telegram API bilgileri
telegram_api_id = '21560699'
telegram_api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'
target_users = ['reccirik',"mefey18","OrhanElmas","nebe18","Mymirzabey57","akman03","Samiay31"]
#################
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
#################
soracaklarim=["Bu bir telegram botu mesajıdır. Grid bactestine baştan başlıyoruz. Grid botu, kaç gün öncesinden başlatsanız, kaç dolar elde ederdiniz, bunu öğreneceksiniz. Lütfen, parantez içlerindeki örnek formatında giriniz. istediğiniz zaman baştan başla yazarak soruları baştan başlatabilirsiniz. \nCoin Çiftini Giriniz (Örn: ONEUSDT): ", "Alt seviyeyi giriniz (Örn: 0.02): ","Üst seviyeyi giriniz (Örn: 0.6): ","Grid sayısını giriniz (alt üst sınır arası kaça bölünsün?) (Binance limit=max 200) (Örn: 200): ","Komisyon yüzdesi (Örn: 0.1 (yani binde bir) (sadece sayı giriniz, yüzde işareti girmeyiniz)): ","Başlangıç sermayesi kaç USDT olsun (Örn. 1000): ","Zaman dilimi ne olsun? (1 dakikalıklarda kontrol etmek için 1m yazınız) (Örn.: 1m, 5m, 1h, 1d): ","Kaç gün önceden itibaren backtest yapalım? (Örn. 45): \n(bu soruyu cevapladıktan sonra lütfen işlemin bitmesini bekleyiniz, cevabınız gelecek. 365 günlük veri işlenmesi yaklaşık 20 dakika sürer...)"]
####################### Grid Backtest Fonksiyonları
def girdiler():
    global symbol
    global start
    global end
    global num_levels
    global comission
    global girilenilkbakiye
    global veriinterval
    global veri_days_back

    global levels
    global geometric_percentage
    global minmiktarondalik
    global myticksize
    global precision_info
    global data_first_close
    global data
    """
    symbol = input("Coin Çiftini Giriniz (Örn: BTCUSDT): ").upper()
    start = float(input("Alt seviyeyi giriniz (Örn: 0.02): "))
    end = float(input("Üst seviyeyi giriniz (Örn: 0.6): "))
    num_levels = int(input("Grid sayısını giriniz (Binance limit=max 200) (Örn: 200): "))
    comission=float(input("Komisyon (Örn: %0.1 (yani binde bir)): %"))
    girilenilkbakiye=int(input("Başlangıç sermayesi kaç USDT olsun (öRN 1000): "))
    veriinterval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    veri_days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))
    """
    data=vericekis(veriinterval,veri_days_back)
    data_first_close=float(data[0][4])

    minmiktarondalik,myticksize,precision_info=get_precision(symbol)
    levels, geometric_percentage = geometric_division(start, end, num_levels)


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

def collect_data(symbol, interval, days_back):
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


def vericekis(veriinterval, veri_days_back):
    # Kullanıcıdan input alma
    #symbol = input("Enter the coin pair (e.g., BTCUSDT): ").strip().upper()
    global symbol
    

    #interval = input("Enter the interval (e.g., 1m, 5m, 1h, 1d): ").strip().lower()
    #days_back = int(input("Enter the number of days back to fetch (e.g. 3): "))

    # Veri toplama
    data = collect_data(symbol, veriinterval, veri_days_back)

    return data
###############




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
    alinacaklar, satilacaklar = split_levels(levels, data_first_close)
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
                        print(f"Hata: {e}")
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
                    #        # place_sell_order(symbol, orderprice, mymyq)
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
            Kaç gündür bot çalışıyor: {veri_days_back} gün
            Gridler arası yüzde: %{geometric_percentage}
            Binance'ta açmak için gerekli min. bakiye: {yavilkbakiyeiste} USDT
            Başlangıç bakiyesi: {girilenilkbakiye} USDT
            Tamamlanmış işlem sayısı: {satimsayisi}
            Gridden elde edilen realized USDT: {round(gridprofit*girilenboluminbakiye, 2)} USDT
            Gridden yüzde kazanç ((Grid kazancı bölü ilk bakiye) * 100): %{round((gridprofit / yavilkbakiyeiste), 2) * 100}
            Şuanki gridden gelen hariç bakiye: {round(yavsonbakiyeiste*girilenboluminbakiye , 2)} USDT
            Şuanki grid dahil bakiye: {round((yavsonbakiyeiste + gridprofit) * girilenboluminbakiye , 2)} USDT
            Şuanki grid dahil bakiye bölü ilk bakiye: {round(kazancorani, 2)} X (yani toplam %{100*(round(kazancorani, 2)-1)} ekstra gelir gelmiş.)
            Bot başlarkenki coin fiyatı: {data_first_close} USDT
            Coin son fiyatı: {data[-1][4]} USDT
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
            
            file_name = f"{symbol}-{veri_days_back}gun-gridKarYuzde{round((gridprofit / yavilkbakiyeiste), 2) * 100}-bakiyeX{round(kazancorani, 2)}-aralikYuzde{geometric_percentage}-{get_current_datetime_text()}"
            create_and_write_txt(file_name, istatistik)
            return istatistik

        else:
            raise ValueError("Data is empty.")
    except Exception as e:
        print(f"Hata: {e}")

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
    alinacaklar, satilacaklar = split_levels(levels, data_first_close)
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

    ilkbakiye= ilkbakiyehesapla()   #myassetsasagi + (mymyq*close)*len(satilacaklar)
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
    return process_close_values(data)
###################### Backtest Fonksiyonları Bitti
#soracaklarim = ["Grid bactestine baştan başlıyoruz. Hangi coin?", "Alt sınır?", "Üst sınır?", "Kaç grid olsun? (bu soruyu cevapladıktan sonra lütfen işlemin bitmesini bekleyiniz, cevabınız gelecek...)"]
user_data = {}


def myanafonk(answers):
    # Kullanıcıdan gelen yanıtları işleyin
    global symbol
    global start
    global end
    global num_levels
    global comission
    global girilenilkbakiye
    global veriinterval
    global veri_days_back
    if "USDT" in answers[0].upper():
        symbol = answers[0].upper()
    else:
        symbol = answers[0].upper() + "USDT"
    start=float(answers[1].replace(",", "."))
    end = float(answers[2].replace(",", "."))
    num_levels = int(answers[3])
    comission = float(answers[4].replace(",", "."))
    girilenilkbakiye = float(answers[5].replace(",", "."))
    veriinterval = answers[6].lower()
    if int(answers[7])>3650:
        veri_days_back=3605
    else:
        veri_days_back = int(answers[7])

    #response = f"\n\nCevaplarınız işlendi:\n" + "\n".join([f"{i+1}. {q}: {a}" for i, (q, a) in enumerate(zip(soracaklarim, answers))])
    return mybacktest()


async def main():
    global user_data
    global target_users

    # Telegram istemcisini başlat
    telegram_client = TelegramClient('session_name', telegram_api_id, telegram_api_hash)

    try:
        await telegram_client.start(phone=phone_number)

        async def send_question(user):
            """Sıradaki soruyu kullanıcıya gönderir."""
            if user not in user_data:
                user_data[user] = {"answers": [], "question_index": 0, "processing": False}

            question_index = user_data[user]["question_index"]

            if question_index < len(soracaklarim):
                await telegram_client.send_message(user, soracaklarim[question_index])
            elif not user_data[user]["processing"]:
                # Tüm sorular soruldu, yanıtları işle
                user_data[user]["processing"] = True
                try:
                    result = await asyncio.to_thread(myanafonk, user_data[user]["answers"])
                    await telegram_client.send_message(user, result)
                except Exception as e:
                    await telegram_client.send_message(user, f"Hata oluştu: {e}")
                finally:
                    # Başlangıç değerlerine dön
                    user_data[user] = {"answers": [], "question_index": 0, "processing": False}
                    await send_question(user)

        @telegram_client.on(events.NewMessage(from_users=target_users))
        async def handle_response(event):
            """Kullanıcıdan gelen yanıtları işler ve özel komutları ele alır."""
            global target_users
            user = event.sender_id
            message = event.raw_text.strip()

            # Yeni kullanıcı ekleme
            if message.startswith("yenikayit-"):
                new_user = message.split("-", 1)[1].strip()
                if new_user not in target_users:
                    target_users.append(new_user)
                    await telegram_client.send_message(event.sender_id, f"Yeni kullanıcı '{new_user}' listeye eklendi.")
                else:
                    await telegram_client.send_message(event.sender_id, f"'{new_user}' zaten listeye kayıtlı.")
                return

            # Kullanıcı silme
            if message.startswith("kullanicisil-"):
                remove_user = message.split("-", 1)[1].strip()
                if remove_user in target_users:
                    target_users.remove(remove_user)
                    user_data.pop(remove_user, None)  # Kullanıcı verilerini de temizle
                    await telegram_client.send_message(event.sender_id, f"'{remove_user}' listeden silindi.")
                else:
                    await telegram_client.send_message(event.sender_id, f"'{remove_user}' zaten listede değil.")
                return

            # Baştan başla komutu
            if message.lower() == "baştan başla":
                if user in user_data:
                    user_data[user] = {"answers": [], "question_index": 0, "processing": False}
                    await telegram_client.send_message(user, "Süreç baştan başlatıldı.")
                    await send_question(user)
                else:
                    await telegram_client.send_message(user, "Kayıtlı bir süreciniz bulunamadı.")
                return

            # Normal mesaj işleme
            if user not in user_data:
                user_data[user] = {"answers": [], "question_index": 0, "processing": False}

            if user_data[user]["processing"]:
                await telegram_client.send_message(user, "Cevabınız üretilirken lütfen bekleyiniz.")
                return

            answer = message
            user_data[user]["answers"].append(answer)
            user_data[user]["question_index"] += 1
            await send_question(user)

        # İlk soruları gönder
        for user in target_users:
            await send_question(user)

        # Botu çalışır durumda tut
        await telegram_client.run_until_disconnected()

    except Exception as e:
        print(f"Bot çalışırken bir hata oluştu: {e}")
        await telegram_client.disconnect()
    finally:
        print("Bot sonlandı. Yeniden başlatılıyor...")
        await main()  # Botun sürekli çalışmasını sağlamak için yeniden başlatma


# Ana döngüyü başlat
if __name__ == "__main__":
    asyncio.run(main())
