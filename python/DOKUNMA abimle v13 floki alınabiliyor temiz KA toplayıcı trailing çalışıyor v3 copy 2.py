#v0dan kopyalandı
from telethon import TelegramClient, events
from binance.client import Client
import asyncio
import re
import random
import time
from binance.enums import *
import requests
import json
#import time
from datetime import datetime
import pandas as pd

# API ayarları
telegram_api_id = '21560699'
telegram_api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'
target_user = 'tradermikabot'  # Hedef kullanıcının kullanıcı adı
alert_user = 'reccirik_bot'  # Bildirim gönderilecek kullanıcı adı
binance_api="PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
binance_secret="iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
binance_api_reccirik2="nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_reccirik2="WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"
binance_api_abim="W0cyfW6O27i7GsBKFYbm4zVjiOE0oY2lbOZYQwbYWksuDZG1zwt10x5w42GQ6JDa"
binance_secret_abim="FdrwJZG7zXTi3qwj9zQaxCb0YFWoYAZexGCTAP2QkUcMhV4dQuq5OGSQYgiQYioE"


################################################## Değişkeler:
#binance future listesi
binanceclient_abim = Client(binance_api_abim, binance_secret_abim)
binanceclient = Client(binance_api, binance_secret)
exchange_info = binanceclient.futures_exchange_info()
symbols = exchange_info['symbols']
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s["symbol"]),
# Telegram Client'ı oluşturun
telegram_client = TelegramClient('session_name', telegram_api_id, telegram_api_hash)
#patterler
pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
pattern2 = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')
patternSDV = r"✅✅(\w+)"
patternSDVtek = r"✅ (\w+)"
patternSDVasagicift = r"🔻🔻(\w+)"
patternSDVasagitek = r"🔻 (\w+)"
patternKA = r'\b(\w+)\s+TS:'
#Global değişkenler
dosya_adi = f"usdtlistem-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
mycost=3.5
myleverage=7
kactanbuyuk=17
#mytextio = ["15m=> %57,2 🔼 1h=> %51,9 🔼 4h=> %52,2 🔼 12h=> %48,5 🔻 1d=> %48,9 🔻 En çok nakit girişi olanlar.(Sonunda 🔼 olanlarda nakit girişi daha sağlıklıdır) Nakitin nereye aktığını gösterir. (Nakit Göçü Raporu) BTC Nakit: %18,8 15m: %68 🔼🔼🔼🔻🔻 XLM Nakit: %11,3 15m: %58 🔼🔼🔼🔼🔼 SOL Nakit: %5,7 15m: %68 🔼🔼🔼🔻🔻 ETH Nakit: %5,4 15m: %59 🔼🔻🔻🔻🔻 DOGE Nakit: %4,6 15m: %45 🔻🔼🔼🔻🔻 XRP Nakit: %4,4 15m: %54 🔼🔼🔼🔻🔻 ADA Nakit: %2,3 15m: %56 🔼🔼🔼🔻🔻 FTM Nakit: %1,8 15m: %78 🔼🔼🔼🔻🔻 USDC Nakit: %1,6 15m: %46 🔻🔻🔼🔼🔼 SAND Nakit: %1,6 15m: %55 🔼🔼🔼🔻🔼 DOT Nakit: %1,6 15m: %66 🔼🔼🔼🔼🔼 PNUT Nakit: %1,5 15m: %50 🔻🔻🔼🔼🔼 NEAR Nakit: %1,3 15m: %59 🔼🔼🔼🔻🔻 PEPE Nakit: %1,3 15m: %62 🔼🔼🔼🔻🔻 LRC Nakit: %1,2 15m: %53 🔼🔼🔼🔼🔼 AVAX Nakit: %1,0 15m: %55 🔼🔼🔼🔻🔻 WLD Nakit: %0,9 15m: %47 🔻🔻🔻🔻🔻 SEI Nakit: %0,9 15m: %59 🔼🔻🔻🔻🔻 FET Nakit: %0,9 15m: %48 🔻🔼🔻🔻🔻 LTC Nakit: %0,8 15m: %65 🔼🔼🔼🔻🔻 WIF Nakit: %0,8 15m: %64 🔼🔼🔼🔻🔻 LINK Nakit: %0,8 15m: %60 🔼🔼🔼🔻🔻 PYR Nakit: %0,8 15m: %55 🔼🔼🔼🔼🔼 BNB Nakit: %0,8 15m: %32 🔻🔻🔻🔻🔻 SHIB Nakit: %0,7 15m: %57 🔼🔼🔼🔻🔼 NOT Nakit: %0,6 15m: %54 🔼🔻🔼🔼🔼 TIA Nakit: %0,6 15m: %43 🔻🔻🔻🔼🔼 SLF Nakit: %0,6 15m: %56 🔼🔼🔼🔼🔼 LDO Nakit: %0,6 15m: %64 🔼🔼🔼🔻🔼 MANA Nakit: %0,5 15m: %62 🔼🔼🔻🔻🔼 Piyasa ciddi anlamda risk barındırıyor. Alım Yapma! Günlük nakit giriş oranı (1d satirindaki değer) %50 üzerine çıkarsa risk azalacaktır. Bu değer %49 altında oldukça piyasaya bulaşma! Kısa vadede tüm coinlere olan nakit girişini beğendim :). Bu modülün mantığını anlamak için bu kelimeye dokun: /EInOut"]
mytextio=["merhaba"]
mylonglar=[]
myshortlar=[]
mylonglarKA=[]
mylonglarSDV=[]
myshortlarSDV=[]
mylonglarCi=[]
myshortlarCi=[]
mylonglarMA=[]
mylonglarIOF=[]
myshortlarIOF=[]
ciraporu=0
karaporu=0
sdvraporu=0
maraporu=0
iofraporu=0
io1d=[49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1,49.1]
altustsinir=[48.1,49.5]
mybuys=[]
mysells=[]
hesapkitap=[]
smaperiod=7
myacc=[]
ilkio=float(input("io rakamını giriniz:"))
ilkkackez=int(input("kaç tane io eklensin?"))
for i in range(1, ilkkackez + 1):
    #print(i)
    io1d.append(ilkio)
cirawtext=[]
acmakapamalistesi=[]
usdtlistem=[]
iopower=[]
yasaklilist=["ETHUSDT","SOLUSDT","BTCUSDT","USDCUSDT"]
symbolstrailingprices=[]
trailingyuzde=7 #yüzde düşünce kapanır.
yuzdekackazanincakapatsin=2000
calissinmi=True


##################################### Yardımcı Fonksiyonlar:
def rastgele_sayi(min_deger, max_deger):
    return random.randint(min_deger, max_deger)

def check_arrowsIO(text):
    # Regex to find the lines with "15m=>", "1h=>" and "4h=>" with downward arrows
    pattern_15m = r'15m=>.*🔻'
    pattern_1h = r'1h=>.*🔻'
    pattern_4h = r'4h=>.*🔻'
    pattern_12h = r'12h=>.*🔻'
    pattern_1d = r'1d=>.*🔻'

    if convert_to_floatIO(text)<49: #or (re.search(pattern_4h, text) and re.search(pattern_12h, text) and re.search(pattern_1d, text)):# (re.search(pattern_15m, text) and re.search(pattern_1h, text) and re.search(pattern_4h, text) and re.search(pattern_12h, text)) or (re.search(pattern_1h, text) and re.search(pattern_4h, text) and re.search(pattern_12h, text) and re.search(pattern_1d, text)):
        print("!!!!!!!!!!!!!!!!!!!!! Piyasa Rikli !!!!!!!!!!!!!!!!!!!")
        return False
    else:
        print(">>>>>>>>>>>>>>>>>>>>>> Piyasa iyi durumda <<<<<<<<<<<<<<<<<<<<<<<<")
        return True


def convert_to_floatIOsure(text,sure):
    # "1d=> %"den hemen sonra gelen sayıyı yakalamak için regex deseni
    pattern1d = r'1d=> %([\d,]+)'
    pattern12h = r'12h=> %([\d,]+)'
    pattern4h = r'4h=> %([\d,]+)'
    pattern1h = r'1h=> %([\d,]+)'
    pattern15m = r'15m=> %([\d,]+)'
    # Eşleşmeyi bul
    match = re.search(pattern1d if sure=="1d" else pattern12h if sure=="12h" else pattern4h if sure=="4h" else pattern1h if sure=="1h" else pattern15m, text)
    if match:
        # Eşleşen kısmı al
        number_str = match.group(1)
        # Virgülü noktaya çevir ve float'a dönüştür
        number_float = float(number_str.replace(',', '.'))
        return number_float
    else:
        return 50

def io15m1h4hdusuktemi():
    if convert_to_floatIOsure(mytextio[0],"15m")<50 and convert_to_floatIOsure(mytextio[0],"1h")<50 and convert_to_floatIOsure(mytextio[0],"4h")<50:
        return True
    else:
        return False

def io15m1h4hyuksektemi():
    if convert_to_floatIOsure(mytextio[0],"15m")>50 and convert_to_floatIOsure(mytextio[0],"1h")>50 and convert_to_floatIOsure(mytextio[0],"4h")>50:
        return True
    else:
        return False

def parse_textMA(text):
    # "15m=>" sonrasını kaldır
    text = text.split("15m=>")[0]
    # Her satırı ayır
    lines = text.split('\n')
    
    results = []
    
    for line in lines:
        if 'USDT' in line:
            # Regex ile USDT'li kelimeyi ve boşluklarla ayrılmış ilk dört sayıyı bul
            matches = re.findall(r'(\b\w*USDT\b).+?(\d+,\d+)\s+(\d+,\d+)\s+(\d+)\s+(\d+,\d+)', line)
            for match in matches:
                # Sayılardaki virgülleri noktaya çevir ve float'a dönüştür
                numbers = [float(num.replace(',', '.')) for num in match[1:]]
                # Sonuçları listeye ekle
                results.append([match[0]] + numbers)
    
    return results

def extract_coin_dataKA(text):
    # "Canlı olan coin sayısı:" kelimesinden sonraki sayıyı bulma
    coin_count_match = re.search(r'Canlı olan coin sayısı:(\d+)', text)
    coin_count = int(coin_count_match.group(1)) if coin_count_match else None
    coin_count2=[coin_count,1.2, 1.1, 1.048, 788, True, 7.3] #['ETHUSDT', 1.2, 1.1, 1.048, 788, True, 7.3]

    # TS, MTS, PT, Dk ve Kar bilgilerinin eşleşmesini bulma
    pattern = r'(\w+)\sTS:(\S+)\sMTS:(\S+)\sPT:(\S+)\s+Dk:(\d+)(✅)?\s+Kar:%(\d+,\d+)'
    matches = re.findall(pattern, text)

    # Elde edilen eşleşmeleri işleyip listeye ekle
    result = [[
        match[0] + 'USDT',
        None if match[1] == 'NULL' else float(match[1].replace(',', '.')),
        float(match[2].replace(',', '.')),
        float(match[3].replace(',', '.')),
        int(match[4]),
        bool(match[5]),
        float(match[6].replace(',', '.'))
    ] for match in matches]

    return [coin_count2] + result

def find_usdt_and_numbersMA15m(text):
    mytext5m=text.split("15m=> Symbol")[0]
    pattern = r'(\b\w+USDT\b).*?(\d{1,3}(?:,\d{1,3})?(?:\.\d+)?).*?(\d{1,3}(?:,\d{1,3})?(?:\.\d+)?).*?(\d{1,3}(?:,\d{1,3})?(?:\.\d+)?).*?(\d{1,3}(?:,\d{1,3})?(?:\.\d+)?)'
    matches = re.findall(pattern, mytext5m)
    results = []
    for match in matches:
        usdt_word = match[0]
        numbers = [float(num.replace(',', '.')) for num in match[1:]]
        results.append([usdt_word] + numbers)

    return results

def get_price(symbol):
    try:
        ticker = binanceclient.get_symbol_ticker(symbol=symbol.upper())
        return ticker['price']
    except Exception as e:
        print(f"Error: {e}")
        return 1

def myquantity(coin):
    return round(((get_my_cost()*myleverage)/float(get_price(coin))),3)

karzararnumber=[]
karzararlistesi=[]
def karzararesapla(coin, quantity, entry, close, liste, pozisyon):
    kar=pozisyon * quantity * (float(close) - float(entry))
    karzararlistesi.append([liste,coin,kar])
    print(f"kar zarar litesi:{karzararlistesi}")
    #mykar=[]
    #for elem in reversed(karzararlistesi):
    #    if elem[1] == coin:
    #        mykar.append(float(k[2]))
    #        #print(elem[1])  # Son "kar" elemanının ikinci değeri
    #        break
    #for k in karzararlistesi:
        
    karzararnumber.append(kar)
    print(kar)
    print(sum(karzararnumber))

def dosyala(karzarardurumu):
    # While döngüsü
    try:
        with open(dosya_adi, "a") as dosya:
            # Dosyaya yeni bir satır ekle
            dosya.write(f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')} Kar-Zarar Durumu: {karzarardurumu}\n")
            print(f"{karzarardurumu}. satır dosyaya eklendi.")
    except KeyboardInterrupt:
        print("\nDöngü durduruldu. Dosya kapatıldı.")

mylonglarGenel=[]
def close_position(coin,liste):
    # Mevcut pozisyonu kapat
    #binanceclient için:
    positions = binanceclient.futures_position_information(symbol=coin)
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            myquantity=abs(float(position['positionAmt']))
            karzararesapla(coin,myquantity,position['entryPrice'],get_price(coin),liste,1 if side=="SIDE_BUY" else -1)
            order = binanceclient.futures_create_order(
                symbol=coin,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=myquantity
            )
            print(f"Pozisyon kapatıldı: {order}")
            if coin in mylonglarGenel:
                    mylonglarGenel.remove(coin)
            mtext=f"Kapatılan Çift: {position['symbol']}, Miktar: {position['positionAmt']}, Giriş Fiyatı: {position['entryPrice']}, Çıkış fiyatı: {get_price(position["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            hesapla(coin, side, myquantity)
            eklesil(coin,liste,"sil")
            time.sleep(5)  # 5 saniye bekle
    # Futures cüzdanındaki USDT miktarını öğren
    account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    usdt_balance = 0

    for asset in account_info['assets']:
        if asset['asset'] == 'USDT':  # USDT bakiyesini bul
            usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)
    print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
    print(usdtlistem)
    print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
    dosyala(usdt_balance)
    if len(usdtlistem)>2:
        dosyala(usdtlistem[-2]-usdtlistem[-1])
    
    #binanceclient_abim için:
    positions_abim = binanceclient_abim.futures_position_information(symbol=coin)
    for position in positions_abim:
        if float(position['positionAmt']) != 0:
            side_abim = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            myquantity_abim=abs(float(position['positionAmt']))
            #karzararesapla(coin,myquantity,position['entryPrice'],get_price(coin),liste,1 if side=="SIDE_BUY" else -1)
            order_abim = binanceclient_abim.futures_create_order(
                symbol=coin,
                side=side_abim,
                type=ORDER_TYPE_MARKET,
                quantity=myquantity_abim
            )
            print(f"Pozisyon kapatıldı: {order_abim}")
            #if coin in mylonglarGenel:
            #    mylonglarGenel.remove(coin)
            #mtext=f"Kapatılan Çift: {position['symbol']}, Miktar: {position['positionAmt']}, Giriş Fiyatı: {position['entryPrice']}, Çıkış fiyatı: {get_price(position["symbol"])}"
            #acmakapamalistesi.append(mtext)
            #print(mtext)
            #hesapla(coin, side, myquantity)
            #eklesil(coin,liste,"sil")
            time.sleep(5)  # 5 saniye bekle

def hesapla(coin, pozisyon, quantity):
    price=get_price(coin)
    if pozisyon=="buy":
        mybuys.append([coin,price])
    elif pozisyon=="sell":
        mysells.append([coin,price])
    elif pozisyon=="SIDE_BUY":
        ind= -1
        for c in mybuys:
            if c[0]==coin:    
                kar=(price * quantity) - (c[1] * quantity)
                hesapkitap.append(kar)
                print(f"Kar: {kar}")
                del mybuys[ind]
    elif pozisyon=="SIDE_SELL":
        ind= -1
        for c in mysells:
            ind+=1
            if c[0]==coin:    
                kar=(c[1] * quantity) - (price * quantity)
                hesapkitap.append(kar)
                print(f"Kar: {kar}")
                del mysells[ind]
        




def get_symbol_precision(symbol):
    try:
        info = binanceclient.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol.upper():
                return int(item['quantityPrecision'])
    except Exception as e:
        print(f"Error: {e}")
        return None

def buy_position(symbol, leverage, amount, liste):
    #if is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
    try:
        binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        
        order = binanceclient.futures_create_order(
            symbol=symbol.upper(),
            side='BUY',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        print(order)
        hesapla(symbol, "buy",1)
        eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")
    try:
        binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision_abim = get_symbol_precision(symbol)
        if precision_abim is None:
            print("Precision could not be determined.")
            return

        quantity_abim = round(amount * leverage / float(binanceclient_abim.get_symbol_ticker(symbol=symbol.upper())['price']), precision_abim)
        
        order_abim = binanceclient_abim.futures_create_order(
            symbol=symbol.upper(),
            side='BUY',
            type='MARKET',
            quantity=quantity_abim,
            leverage=leverage
        )
        print(order)
        #hesapla(symbol, "buy",1)
        #eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")

def sell_position(symbol, leverage, amount, liste):
    #•if not is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
    try:
        binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        
        order = binanceclient.futures_create_order(
            symbol=symbol.upper(),
            side='SELL',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        print(order)
        hesapla(symbol,"sell",1)
        eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")
    try:
        binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision_abim = get_symbol_precision(symbol)
        if precision_abim is None:
            print("Precision could not be determined.")
            return

        quantity_abim = round(amount * leverage / float(binanceclient_abim.get_symbol_ticker(symbol=symbol.upper())['price']), precision_abim)
        
        order_abim = binanceclient_abim.futures_create_order(
            symbol=symbol.upper(),
            side='SELL',
            type='MARKET',
            quantity=quantity_abim,
            leverage=leverage
        )
        print(order_abim)
        #hesapla(symbol,"sell",1)
        #eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")


def convert_to_floatIO(text):
    # "1d=> %"den hemen sonra gelen sayıyı yakalamak için regex deseni
    pattern = r'1d=> %([\d,]+)'
    # Eşleşmeyi bul
    match = re.search(pattern, text)
    if match:
        # Eşleşen kısmı al
        number_str = match.group(1)
        # Virgülü noktaya çevir ve float'a dönüştür
        number_float = float(number_str.replace(',', '.'))
        return number_float
    else:
        return 49.1

def parse_usdt_dataIOF(text):
    pattern = r"([A-Z]+USDT)\s([\d,]+)X\sPayı:%([\d,]+)\sPahalılık:([\d,]+)\s([🔼🔻]{5})"
    matches = re.findall(pattern, text)
    
    result = []
    for match in matches:
        symbol = match[0]
        entry_before_x = float(match[1].replace(",", "."))
        pay_before_percentage = float(match[2].replace(",", "."))
        before_pahalilik = float(match[3].replace(",", "."))
        trend_list = [True if ch == '🔼' else False for ch in match[4]]
        
        result.append([symbol, entry_before_x, pay_before_percentage, before_pahalilik, trend_list])
    
    return result

def binle(coin):
    liste=["BONKUSDT","FLOKIUSDT","SATSUSDT","RATUSDT","PEPEUSDT","SHIBUSDT","CATUSDT","XUSDT","LUNCUSDT","XECUSDT"]
    for c in liste:
        if coin == c:
            return ("1000" + c)
        else:
            return coin

def acabilirmiyim(coin):
    if coin in mylonglarSDV or coin in mylonglarCi or coin in mylonglarKA or coin in mylonglarMA or coin in mylonglarIOF or coin in myshortlarCi or coin in myshortlarIOF or coin in myshortlarSDV:
        return False
    else:
        return True         

def longlarikapat():
    for coin in mylonglarCi:
        close_position(coin,"mylonglarCi")
        print(f"{coin} pozisyonu kapatıldı.")
        #mylonglarCi.remove(coin)
    for coin in mylonglarSDV:
        close_position(coin, "mylonglarSDV")
        print(f"{coin} pozisyonu kapatıldı.")
        #mylonglarSDV.remove(coin)
    for coin in mylonglarMA:
        close_position(coin,"mulonglarMA")
        print(f"{coin} pozisyonu kapatıldı.")
        #mylonglarMA.remove(coin)
    for coin in mylonglarKA:
        close_position(coin,"mylonglarKA")
        print(f"{coin} pozisyonu kapatıldı.")
        #mylonglarKA.remove(coin)
    for coin in mylonglarIOF:
        close_position(coin,"mylonglarIOF")
        print(f"{coin} pozisyonu kapatıldı.")
        #mylonglarIOF.remove(coin)

def shortlarikapat():
    for coin in myshortlarCi:
        close_position(coin,"myshortlarCi")
        print(f"{coin} pozisyonu kapatıldı.")
        #myshortlarCi.remove(coin)
    for coin in myshortlarSDV:
        close_position(coin,"myshortlarSDV")
        print(f"{coin} pozisyonu kapatıldı.")
        #myshortlarSDV.remove(coin)
    for coin in myshortlarIOF:
        close_position(coin,"myshortlarIOF")
        print(f"{coin} pozisyonu kapatıldı.")
        #myshortlarIOF.remove(coin)

def sartlaruygunmu():
    if io1d[len(io1d)-1]<altustsinir[0] or io1d[len(io1d)-1]>altustsinir[1]:
        return True
    else:
        return False

def is_above_last_period_average(num, lst, period):
    # Son 7 elemanı al
    last_7 = lst[-period:]
    # Son 7 elemanın ortalamasını hesapla
    average = sum(last_7) / len(last_7) if last_7 else 49.1
    # Sayı ortalamadan büyükse True, değilse False döndür
    return num >= average


def eklesil(coin, liste, eylem):
    if eylem=="ekle":
        if liste=="mylonglarKA" and not coin in mylonglarKA:
            mylonglarKA.append(coin)
        elif liste=="mylonglarSDV" and not coin in mylonglarSDV:
            mylonglarSDV.append(coin)
        elif liste=="mylonglarMA" and not coin in mylonglarMA:
            mylonglarMA.append(coin)
        elif liste=="mylonglarIOF" and not coin in mylonglarIOF:
            mylonglarIOF.append(coin)
        elif liste=="mylonglarCi" and not coin in mylonglarCi:
            mylonglarCi.append(coin)
        elif liste=="myshortlarSDV" and not coin in myshortlarSDV:
            myshortlarSDV.append(coin)
        elif liste=="myshortlarCi" and not coin in myshortlarCi:
            myshortlarCi.append(coin)
        elif liste=="myshortlarIOF" and not coin in myshortlarIOF:
            myshortlarIOF.append(coin)
    if eylem=="sil":
        if liste=="mylonglarKA" and coin in mylonglarKA:
            mylonglarKA.remove(coin)
        elif liste=="mylonglarSDV" and coin in mylonglarSDV:
            mylonglarSDV.remove(coin)
        elif liste=="mylonglarMA" and coin in mylonglarMA:
            mylonglarMA.remove(coin)
        elif liste=="mylonglarIOF" and coin in mylonglarIOF:
            mylonglarIOF.remove(coin)
        elif liste=="mylonglarCi" and coin in mylonglarCi:
            mylonglarCi.remove(coin)
        elif liste=="myshortlarSDV" and coin in myshortlarSDV:
            myshortlarSDV.remove(coin)
        elif liste=="myshortlarCi" and coin in myshortlarCi:
            myshortlarCi.remove(coin)
        elif liste=="myshortlarIOF" and coin in myshortlarIOF:
            myshortlarIOF.remove(coin)

def get_future_total_usdt_balance():
    # Hesap bilgilerinizi alın
    futures_balance = binanceclient.futures_account_balance() 
    for balance in futures_balance: 
        if balance['asset'] == 'USDT':
            # İstediğiniz varlığı buraya girin 
            print(f"Available Balance: {balance['balance']}")
            return float(balance['balance'])
        else:
            return 100
        
get_future_total_usdt_balance()

def get_my_cost():
    return (get_future_total_usdt_balance() * 0.05)

def IOkucuksekapat(sayi):
    if sayi<49.5:
        positions = binanceclient.futures_position_information()
        usdt_positions = [
        pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
        ]
        myacikusdtlist=[]
        for pos in usdt_positions:
            myacikusdtlist.append(pos['symbol'])
            close_position(pos["symbol"], "mylonglarKA")
            print(f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
        #return myacikusdtlist
        # Futures cüzdanındaki USDT miktarını öğren
        account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
        usdt_balance = 0

        for asset in account_info['assets']:
            if asset['asset'] == 'USDT':  # USDT bakiyesini bul
                usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
        usdtlistem.append(usdt_balance)
        print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
        print(usdtlistem)
        print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
        dosyala(usdtlistem[0]-usdtlistem[-1])

def yuvarla_0_5(sayi): # Sayıyı 0.5'in katlarına yuvarla 
    return round(sayi * 2) / 2


###################### EMA ###########################
def ema_hesapla(liste, span):
    """
    EMA hesaplayan bir fonksiyon.
    :param liste: Fiyat listesi
    :param span: EMA periyodu
    :return: EMA değeri
    """
    alpha = 2 / (span + 1)  # Smoothing factor
    ema = liste[0]  # İlk EMA değeri, ilk fiyatla başlar
    
    for fiyat in liste[1:]:
        ema = alpha * fiyat + (1 - alpha) * ema
    
    return ema

def cift_ema_sinyal(liste, kisa_span=2, uzun_span=5):
    """
    Çift EMA kullanarak al/sat sinyali döndüren bir fonksiyon.
    :param liste: Fiyat listesi
    :param son_fiyat: Listeye dahil edilmemiş en son fiyat
    :param kisa_span: Kısa periyot
    :param uzun_span: Uzun periyot
    :return: True (AL) veya False (SAT)
    """
    # EMA'ları hesapla
    kisa_ema = ema_hesapla(liste, kisa_span)
    uzun_ema = ema_hesapla(liste, uzun_span)
    
    # Sinyal oluştur
    #return kisa_ema > uzun_ema  # Kısa EMA uzun EMA'dan büyükse AL (True), aksi halde SAT (False)
    return [io1d[-1]>uzun_ema, io1d[-1]<uzun_ema]

# Örnek veri
#fiyat_listesi = [100, 102, 101, 103, 104, 106, 105, 107, 108, 110, 111, 112, 113]
#son_fiyat = 114

# Çift EMA sinyali
#sinyal = cift_ema_sinyal(fiyat_listesi)
#print(f"Sinyal: {'AL' if sinyal else 'SAT'}")

######################################################

def closelongs():
    positions = binanceclient.futures_position_information()
    usdt_positions = [
    pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
    ]
    myacikusdtlist=[]
    account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    usdt_balance = 0
    
    for asset in account_info['assets']:
        if asset['asset'] == 'USDT':  # USDT bakiyesini bul
            usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)

    for pos in usdt_positions:
        if float(pos['positionAmt']) > 0:
            myacikusdtlist.append(pos['symbol'])
            close_position(pos["symbol"], "mylonglarKA")
            symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (pos["Symbol"],1),True)
            print(f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
            mtext=f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}, Çıkış fiyatı: {get_price(pos["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            time.sleep(7)  # 5 saniye bekle
    #return myacikusdtlist
    # Futures cüzdanındaki USDT miktarını öğren
    account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    usdt_balance = 0
    
    for asset in account_info['assets']:
        if asset['asset'] == 'USDT':  # USDT bakiyesini bul
            usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)
    print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
    print(usdtlistem)
    print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
    dosyala(usdtlistem[-2]-usdtlistem[-1])
    mylonglarCi.clear()
    mylonglarIOF.clear()
    mylonglarKA.clear()
    mylonglarMA.clear()
    mylonglarSDV.clear()

def closeshorts():
    #SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
    account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    usdt_balance = 0

    for asset in account_info['assets']:
        if asset['asset'] == 'USDT':  # USDT bakiyesini bul
            usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)

    positions = binanceclient.futures_position_information()
    usdt_positions = [
    pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
    ]

    myacikusdtlist=[]
    for pos in usdt_positions:
        if float(pos['positionAmt']) < 0:
            myacikusdtlist.append(pos['symbol'])
            close_position(pos["symbol"], "myshortlarKA")
            print(f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
            mtext=f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}, Çıkış fiyatı: {get_price(pos["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            time.sleep(7)  # 5 saniye bekle
    #return myacikusdtlist
    # Futures cüzdanındaki USDT miktarını öğren
    account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    usdt_balance = 0

    for asset in account_info['assets']:
        if asset['asset'] == 'USDT':  # USDT bakiyesini bul
            usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)
    print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
    print(usdtlistem)
    print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
    dosyala(usdtlistem[-2]-usdtlistem[-1])
    myshortlarCi.clear()
    myshortlarIOF.clear()
    myshortlarSDV.clear()

    
def IOdusuyorsakapat(): #longlar kapanacak
    if not is_above_last_period_average(io1d[-1],io1d,smaperiod):
        positions = binanceclient.futures_position_information()
        usdt_positions = [
        pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
        ]
        myacikusdtlist=[]
        for pos in usdt_positions:
            if float(pos['positionAmt']) > 0:
                myacikusdtlist.append(pos['symbol'])
                close_position(pos["symbol"], "mylonglarKA")
                print(f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
                time.sleep(7)  # 5 saniye bekle
        #return myacikusdtlist
            # Futures cüzdanındaki USDT miktarını öğren
        account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
        usdt_balance = 0

        for asset in account_info['assets']:
            if asset['asset'] == 'USDT':  # USDT bakiyesini bul
                usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
        usdtlistem.append(usdt_balance)
        print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
        print(usdtlistem)
        print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
        dosyala(usdtlistem[0]-usdtlistem[-1])

def IOcikiyorsakapat(): #shortlar kapanacak
    if is_above_last_period_average(io1d[-1],io1d,smaperiod):
        #SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
        positions = binanceclient.futures_position_information()
        usdt_positions = [
        pos for pos in positions if pos['symbol'].endswith('USDT') and float(pos['positionAmt']) != 0
        ]
        myacikusdtlist=[]
        for pos in usdt_positions:
            if float(pos['positionAmt']) < 0:
                myacikusdtlist.append(pos['symbol'])
                close_position(pos["symbol"], "myshortlarKA")
                print(f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}")
                time.sleep(7)  # 5 saniye bekle
        #return myacikusdtlist
            # Futures cüzdanındaki USDT miktarını öğren
        account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
        usdt_balance = 0

        for asset in account_info['assets']:
            if asset['asset'] == 'USDT':  # USDT bakiyesini bul
                usdt_balance = float(asset['availableBalance'])  # Kullanılabilir bakiye
    usdtlistem.append(usdt_balance)
    print(f"Futures hesabındaki kullanılabilir USDT miktarı: {usdt_balance}")
    print(usdtlistem)
    print(f"Program başlangıcından şu ana kadarki fark: {usdtlistem[0]-usdtlistem[-1]} USDT")
    dosyala(usdtlistem[0]-usdtlistem[-1])

def hepsi_esit_degil_mi(liste):
    return not all(x == liste[0] for x in liste) if liste else True
    # Örnek kullanım:
    #print(hepsi_esit_mi([3, 3, 3]))  # False
    #print(hepsi_esit_mi([3, 2, 3]))  # True
    #print(hepsi_esit_mi([]))         # True

def ortalamayagorepozisyonacayimmi(pozisyon):
    # Son 7 elemanı al
    last_7 = io1d[(-1*smaperiod):]
    # Son 7 elemanın ortalamasını hesapla
    average = sum(last_7) / len(last_7) if last_7 else io1d[-1]
    # Sayı ortalamadan büyükse True, değilse False döndür
    if io1d[-1]==50:
        return False
    #elif not hepsi_esit_degil_mi(last_7):
    #    return False
    elif pozisyon=="long":    
        return io1d[-1] > average
    elif pozisyon=="short":    
        return io1d[-1] < average
    else: #if pozisyon=="aynimi" and not hepsi_esit_degil_mi(last_7):
        return False

def extract_market_buying_power(text):
    # Regex pattern to capture the number after "Kısa Vadeli Market Alım Gücü:"
    pattern = r"Kısa Vadeli Market Alım Gücü:\s([\d,]+)"
    match = re.search(pattern, text)
    if match:
        # Replace comma with dot and convert to float
        value = match.group(1).replace(',', '.')
        return float(value)
    else:
        raise ValueError("Kısa Vadeli Market Alım Gücü bulunamadı.")

def extract_floatsIOpowerandday(text):
    # "Kısa Vadeli Market Alım Gücü" değerini bul ve dönüştür
    start_power = text.find("Kısa Vadeli Market Alım Gücü: ") + len("Kısa Vadeli Market Alım Gücü: ")
    end_power = text.find("X", start_power)
    short_term_power = float(text[start_power:end_power].replace(",", "."))

    # "1d=> %" değerini bul ve dönüştür
    start_1d = text.find("1d=> %") + len("1d=> %")
    end_1d = text.find(" 🔼", start_1d) if " 🔼" in text[start_1d:] else text.find(" 🔻", start_1d)
    one_day_percent = float(text[start_1d:end_1d].replace(",", "."))

    return [short_term_power, one_day_percent]

def extract_trend_directionsIO(text):
    # İlgili süreleri tanımla
    timeframes = ["15m", "1h", "4h", "12h", "1d"]
    directions = []

    # Metni satır satır işle
    lines = text.splitlines()
    for line in lines:
        # Eğer satır belirtilen zaman dilimlerinden biriyle başlıyorsa
        for timeframe in timeframes:
            if line.strip().startswith(timeframe):
                # Yön işaretini bul ve True/False olarak ekle
                if "🔼" in line:
                    directions.append(True)
                elif "🔻" in line:
                    directions.append(False)
                break  # Zaman dilimi eşleştiğinde döngüden çık

    return directions

############################ kar zarar durumu
# Açık pozisyonları al
def get_futures_positions():
    try:
        # Binance Futures account position endpoint
        account_info = binanceclient.futures_account()
        positions = account_info['positions']

        result = []
        for position in positions:
            # Sadece açık pozisyonları kontrol et (pozisyon miktarı 0'dan farklı olmalı)
            if float(position['positionAmt']) != 0:
                symbol = position['symbol']
                position_amt = float(position['positionAmt'])
                entry_price = float(position['entryPrice'])
                #mark_price = float(position['markPrice'])
                mark_price=float(get_price(symbol))
                leverage = int(position['leverage'])

                # P&L hesaplama
                pnl = (mark_price - entry_price) / entry_price * 100 * (1 if position_amt > 0 else -1)
                result.append({
                    'Symbol': symbol,
                    'Position': position_amt,
                    'Entry Price': entry_price,
                    'Mark Price': mark_price,
                    'Leverage': leverage,
                    'P&L (%)': round(pnl, 2)
                })

        return result

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []

# Pozisyonları listele
positions = get_futures_positions()
print(positions)
if positions:
    print("Açık Pozisyonlar:")
    for pos in positions:
        print(pos)
else:
    print("Açık pozisyon bulunamadı.")
#############################################

def coin_veri_islemeKA(metin):
    pattern = re.compile(r"(\w+)\sTS:[\w,\.]*\sMTS:([\d,]+)\sPT:([\d,]+)\s.*Kar:%([\d,\-]+)")
    matches = pattern.findall(metin)

    result = []

    for match in matches:
        coin = match[0] + "USDT"
        mts = float(match[1].replace(",", "."))
        pt = float(match[2].replace(",", "."))
        kar = float(match[3].replace(",", "."))
        result.append([coin, mts, pt, kar])

    return result

def fiyat_kontrolu(yuzde, fiyat_listesi):
    # En yüksek fiyatı bul
    en_yuksek_fiyat = float(max(fiyat_listesi))
    
    # En son eklenen fiyatı al
    son_eklenen_fiyat = float(fiyat_listesi[-1])
    
    # Yüzde olarak düşüş miktarını hesapla
    yuzde_fiyat_dususu = en_yuksek_fiyat * (float(yuzde) / 100)
    
    # Son eklenen fiyat, en yüksek fiyatın %yüzde kadar altındaysa True döndür
    if en_yuksek_fiyat - son_eklenen_fiyat >= yuzde_fiyat_dususu:
        return True
    else:
        return False
    
###

def fiyat_guncelle(kripto_listesi, yeni_veri, sil=False):
    # yeni_veri: ("BTCUSDT", 50000) gibi bir tuple
    kripto_cifti, fiyat = yeni_veri
    
    # Kripto çiftinin listede olup olmadığını kontrol et
    for kripto in kripto_listesi:
        if kripto[0] == kripto_cifti:
            if sil:
                # Kripto çiftini ve fiyat bilgilerini sil
                kripto_listesi.remove(kripto)
            else:
                # Kripto çifti bulundu, yeni fiyatı float olarak ekle
                kripto[1].append(float(fiyat))
            return kripto_listesi
    
    # Kripto çifti listede yoksa ve silme işlemi yapılmıyorsa, yeni bir eleman ekle
    if not sil:
        kripto_listesi.append([kripto_cifti, [float(fiyat)]])
    return kripto_listesi
"""
# Örnek kullanım
kripto_listesi = [
    ["BTCUSDT", [48000.0, 49000.0]],
    ["ETHUSDT", [1500.0, 1600.0]]
]

# Yeni fiyat ekleme
yeni_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Yeni kripto çifti ekleme
yeni_veri = ("XRPUSDT", 1.2)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Kripto çifti ve fiyat bilgilerini silme
sil_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, sil_veri, sil=True)
print(kripto_listesi)
   
    
    # yeni_veri: ("BTCUSDT", 50000) gibi bir tuple
    kripto_cifti, fiyat = yeni_veri
    
    # Kripto çiftinin listede olup olmadığını kontrol et
    for kripto in kripto_listesi:
        if kripto[0] == kripto_cifti:
            if sil:
                # Kripto çiftini ve fiyat bilgilerini sil
                kripto_listesi.remove(kripto)
            else:
                # Kripto çifti bulundu, yeni fiyatı ekle
                kripto[1].append(fiyat)
            return kripto_listesi
    
    # Kripto çifti listede yoksa ve silme işlemi yapılmıyorsa, yeni bir eleman ekle
    if not sil:
        kripto_listesi.append([kripto_cifti, [fiyat]])
    return kripto_listesi

# Örnek kullanım
kripto_listesi = [
    ["BTCUSDT", [48000, 49000]],
    ["ETHUSDT", [1500, 1600]]
]

# Yeni fiyat ekleme
yeni_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Yeni kripto çifti ekleme
yeni_veri = ("XRPUSDT", 1.2)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Kripto çifti ve fiyat bilgilerini silme
sil_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, sil_veri, sil=True)
print(kripto_listesi)
"""

def fiyat_dalgalanma_takip(symbols_trailing_prices, yuzde):
    dusen_coinler = []
    for coin in symbols_trailing_prices:
        symbol, prices = coin
        max_fiyat = max(prices)
        son_fiyat = prices[-1]
        if (max_fiyat - son_fiyat) / max_fiyat * 100 > yuzde:
            dusen_coinler.append(symbol)
    return dusen_coinler

mymesaj=["naber"]
async def mesajgonder(mesaj,alici):
    await telegram_client.send_message(alici, mesaj)



##############

def check_btcusdt_drop():
    # BTCUSDT için 15 dakikalık mum verilerini al
    klines = binanceclient.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE, limit=4)
    
    # Kapanış fiyatlarını al
    close_prices = [float(kline[4]) for kline in klines]
    
    # Kapanış fiyatlarını pandas Series'e dönüştür
    data = pd.Series(close_prices)
    
    # Yüzde değişimleri hesapla
    percentage_changes = data.pct_change() * 100
    
    # Son 4 periyotta %1'den fazla düşüş olup olmadığını kontrol et
    if (percentage_changes < -1).all():
        return True
    else:
        return False

# Ana fonksiyondakiler: ############################################################################
def AnaFonkIO(raw_text):
    global symbolstrailingprices
    global calissinmi
    calissinmi=False
        
    
    #if check_btcusdt_drop():
    #    closelongs
    
    mytextio.clear()
    mytextio.append(raw_text)
    io1d.append(convert_to_floatIO(mytextio[0]))
    iopower.append(extract_market_buying_power(mytextio[0]))
    mytrend=extract_trend_directionsIO(mytextio[0])
    new_list=io1d[:]
    new_list.pop()
    if io1d[-1]>50.1 or (cift_ema_sinyal(io1d)[0] and cift_ema_sinyal(new_list)[1]):
        #closeshorts() #shortlar kapanacak
        print("shortları kapatmalı")
    if io1d[-1]<49.9 or (not mytrend[0] and not mytrend[1] and not mytrend[2]) or (cift_ema_sinyal(io1d)[1] and cift_ema_sinyal(new_list)[0]):
        #closelongs() #longlar kapanacak
        print("longları kapatmalı")
    
    
    #if not ortalamayagorepozisyonacayimmi("aynimi"):
    #    closeshorts() #shortlar kapanacak
    #    closelongs() #longlar kapanacak
        
    #if io15m1h4hdusuktemi():
    #    closelongs()
    #elif io15m1h4hyuksektemi(): #convert_to_floatIOsure(raw_text,"15m")>50 and convert_to_floatIOsure(raw_text,"1h")>50 and convert_to_floatIOsure(raw_text,"4h")>50:
    #    closeshorts()
    #IOkucuksekapat(io1d[-1])
    #IOdusuyorsakapat()
    print(f"Longlar:\nCi:{mylonglarCi}\nIOF:{mylonglarIOF}\nSDV:{mylonglarSDV}\nKA:{mylonglarKA}\nMA:{mylonglarMA}")
    print(f"Shortlar:\nCi:{myshortlarCi}\nIOF:{myshortlarIOF}\nSDV:{myshortlarSDV}")  
    print(f"IOs:{io1d}")   
    print(f"Kar zinciri: {hesapkitap}")      
    toplamkarzarar=sum(hesapkitap) 
    print(f"Toplam kar zarar: {toplamkarzarar}")
    print(f"IO 1d, yukarı trendde mi?: {cift_ema_sinyal(io1d)[0]}")

    # Pozisyonları listele
    positions = get_futures_positions()
    kapatılacaklar=[]
    karzarardurumu=[]
    tsymbol=[]
    tprice=[]
    io49unaltinda=[]
    if positions:
        print("Açık Pozisyonlar:")
        for pos in positions:
            print(pos)
            if pos["P&L (%)"]>(yuzdekackazanincakapatsin) or pos["P&L (%)"]<(-1*trailingyuzde):
                kapatılacaklar.append([pos["Symbol"],pos["Mark Price"]])
            kar=pos["Position"]*pos["Entry Price"]*pos['P&L (%)']*0.01
            #print(kar)
            karzarardurumu.append(kar)
            tsymbol.append(pos["Symbol"])
            if io1d[-1]<49:
                io49unaltinda.append(pos["Symbol"])
            myp=get_price(pos["Symbol"])
            tprice.append(myp)
            symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (pos["Symbol"],myp))
    else:
        print("Açık pozisyon bulunamadı.")


    for c in kapatılacaklar:
        mymesaj.append(c[0])
        close_position(c[0],"mylonglarKA")
        symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (c[0],c[1]),True)
        time.sleep(8)

    for c in io49unaltinda:
        mymesaj.append(c)
        close_position(c,"mylonglarKA")
        symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (c,1),True)
        time.sleep(8)

    #{'Symbol': 'ORDIUSDT', 'Position': 0.3, 'Entry Price': 44.203, 'Mark Price': 44.35, 'Leverage': 4, 'P&L (%)': 0.33}
    print(f"Şuanki açık pozisyonların toplam kar zarar durumu: {round(sum(karzarardurumu),2)} USDT")
    #print("Açık pozisyonlar ve fiyat takibi:")
    #for c in symbolstrailingprices:
    #    print(c)
    #print(f"symbolstrailingprices: {symbolstrailingprices}")
    #############################
    trailing_dusen_coinler = fiyat_dalgalanma_takip(symbolstrailingprices, trailingyuzde)
    print(f" trailing düşen coinler: {trailing_dusen_coinler}")
    if trailing_dusen_coinler:
        #telegram_client.send_message(alert_user, f"{trailing_dusen_coinler} trailing stop ile kapatılan coinler.")
        for coin in trailing_dusen_coinler:
            close_position(coin,"mylonglarKA")
            mymesaj.append(coin)
            symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (coin,1.1),True)
            time.sleep(8)
    calissinmi=True
    """
    
    if symbolstrailingprices:
        gecicistp=symbolstrailingprices[:]
        if gecicistp:
            for stp in gecicistp:
                for s in range(len(tsymbol)):
                    if tsymbol[s]==stp[0]:
                        stp.append(tprice[s])
    for i in range(len(tsymbol)):
        if gecicistp:
            for stp in gecicistp:
                if tsymbol[i]==stp[0]:
                    continue
                else:
                    gecicistp.append([tsymbol[i],tprice[i]])
        else:
            gecicistp.append([tsymbol[i],tprice[i]])
        
    
    """


    #mesajgonder(f"{trailing_dusen_coinler} trailing stop ile kapatılan coinler.", alert_user)
    
    ##########################
    
    """
    gecicistp = []

    if symbolstrailingprices:
        gecicistp = symbolstrailingprices[:]
        if gecicistp:
            for stp in gecicistp:
                for s in range(len(tsymbol)):
                    if tsymbol[s] == stp[0]:
                        stp.append(float(tprice[s]))

    for i in range(len(tsymbol)):
        if gecicistp:
            for stp in gecicistp:
                if tsymbol[i] == stp[0]:
                    continue
                else:
                    gecicistp.append([tsymbol[i], float(tprice[i])])
        else:
            gecicistp.append([tsymbol[i], float(tprice[i])])

    mytrailingkapatilacaklar = []
    for stp in gecicistp:
        yeni_liste = stp[1:]
        if fiyat_kontrolu(trailingyuzde, yeni_liste):
            mytrailingkapatilacaklar.append(stp[0])
            close_position(stp[0], "mylonglarKA")

    if mytrailingkapatilacaklar:
        for s in mytrailingkapatilacaklar:
            yenistpl = [stp for stp in gecicistp if stp[0] != s]
            gecicistp = yenistpl[:]

    if gecicistp:
        symbolstrailingprices = gecicistp[:]
    print(symbolstrailingprices)
    
    # Örnek kullanım
    def fiyat_kontrolu(trailingyuzde, yeni_liste):
        # Örnek kontrol fonksiyonu
        return True

    def close_position(symbol, position_type):
        # Örnek kapatma fonksiyonu
        print(f"Pozisyon kapatıldı: {symbol}, {position_type}")

    # Örnek veriler
    tsymbol = ["BTC", "ETH", "XRP"]
    tprice = [50000, 4000, 1]
    trailingyuzde = 0.05

    myfonk(tsymbol, tprice, trailingyuzde)
    """
    ##########################
    if io1d[-1]-io1d[-2]>0.2 or io1d[-2]-io1d[-1]>0.19:
        print("BALİNAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if False:
        if io1d[len(io1d)-1]>altustsinir[1] and not io1d[len(io1d)-2]>altustsinir[1]:
            shortlarikapat()
        elif io1d[len(io1d)-1]<altustsinir[1] and not io1d[len(io1d)-2]<altustsinir[1]:
            longlarikapat()
        elif io1d[len(io1d)-1]<altustsinir[0] and not io1d[len(io1d)-2]<altustsinir[0]:
            longlarikapat()
        elif io1d[len(io1d)-1]>altustsinir[0] and not io1d[len(io1d)-2]<altustsinir[0]:
            shortlarikapat()
        
        if not check_arrowsIO(mytextio[0]): #re.search(pattern_15m, event.raw_text) and re.search(pattern_1h, event.raw_text) and re.search(pattern_4h, event.raw_text):
            print("Piyasa riskli!!!!!!!!!!!!!!!!!")
            if len(mylonglarKA)>0:
                for coin in mylonglarKA:
                    close_position(coin,"mylonglarKA")
                    print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarKA.remove(coin)
                    #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
            if len(mylonglarMA)>0:
                for coin in mylonglarMA:
                    close_position(coin,"mylonglarMA")
                    print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarMA.remove(coin)
                    #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
            if len(mylonglarSDV)>0:    
                for coin in mylonglarSDV:
                    close_position(coin,"mylonglarSDV")
                    print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarSDV.remove(coin)
                    #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
            if len(mylonglarIOF)>0:    
                for coin in mylonglarIOF:
                    close_position(coin,"mylonglarIOF")
                    print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarIOF.remove(coin)
                    #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
            if len(mylonglarCi)>0:    
                for coin in mylonglarCi:
                    close_position(coin,"mylonglarCi")
                    print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarCi.remove(coin)
                    #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        else:
            print("piyasa iyi durumda.>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")
        print(f"Longlar:\nCi:{mylonglarCi}\nIOF:{mylonglarIOF}\nSDV:{mylonglarSDV}\nKA:{mylonglarKA}\nMA:{mylonglarMA}")
        print(f"Shortlar:\nCi:{myshortlarCi}\nIOF:{myshortlarIOF}\nSDV:{myshortlarSDV}")  
        print(f"IOs:{io1d}")   
        print(f"Kar zinciri: {hesapkitap}")      
        toplamkarzarar=sum(hesapkitap) 
        print(f"Toplam kar zarar: {toplamkarzarar}")
        print(f"IO 1d, yukarı trendde mi?: {is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod)}")
    print("temiz KA toplayıcı trailing çalışıyor v3.py")

def AnaFonkKA(raw_text):
    global calissinmi
    calissinmi=False
    #[1,???], ['ETHUSDT', 1.2, 1.1, 1.048, 788, True, 7.3]
    #TRX TS:1,6 MTS:1,4 PT:1,048 Dk:288✅ Kar:%7,6 😍 Grafik (http://tradingview.com/chart/?symbol=BINANCE:TRXUSDT)
    #v2:
    #STRK TS:NULL MTS:1,8 PT:1,051 Dk:18✅ Kar:%-0,6 🤕
    #['STRKUSDT', 1.8, 1.051, -0.6]
    result = coin_veri_islemeKA(raw_text)
    #print(result)
    if io1d[-1]>48.9: #result[0][0]>-1:# and io1d[-1]>50.1 and (extract_market_buying_power(mytextio[0])>1 or cift_ema_sinyal(iopower)[0]) and cift_ema_sinyal(io1d)[0]:#and cift_ema_sinyal(io1d)[0] and io1d[-1]!=49.9 and io1d[-1]!=50 and io1d[-1]!=50.1: # and not io15m1h4hdusuktemi():
        myFKAlist=[]
        kadakilonglar=[]
        for coin in result:
            print(coin[0],coin[1],coin[2], coin[3])
            if binle(coin[0]) in mysymbols3 and coin[1]<1.7 and coin[1]>1.1 and coin[2]>1.005 and coin[3]<7 and acabilirmiyim(binle(coin[0])):
                myFKAlist.append(binle(coin[0]))
            if binle(coin[0]) in mysymbols3:
                kadakilonglar.append(binle(coin[0]))
        
        for coin in myFKAlist:
            if coin in mylonglarKA:
                print(f"{coin} zaten vardı")
            elif coin in yasaklilist:
                print(f"Açılamayan coin: {coin}")
            else:
                #mylonglarKA.append(coin)
                buy_position(coin, myleverage, get_my_cost(), "mylonglarKA")
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        
        """
        for coin in mylonglarKA:
            if coin in kadakilonglar:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarKA")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarKA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print(f"Longlar:{mylonglarKA}")
        """
    else:
        print("io1d<altustsinir[1]")
    calissinmi=True

def AnaFonkMA(raw_text):
    #matchesMA = re.findall(patternMA2, event.raw_text)
    #resultMA = [[match[0], float(match[1].replace(',', '.')), float(match[2].replace(',', '.')), float(match[3]), float(match[4].replace(',', '.'))] for match in matchesMA]
    
    if "Btc düşüş trendinde olduğu için," in raw_text:
        for coin in mylonglarMA:
            close_position(coin,"mylonglarMA")
            print(f"{coin} pozisyonu kapatıldı.")
            #mylonglarMA.remove(coin)
            #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print("Btc düşüş trendinde olduğu için, çalışmadı.")

    elif io1d[len(io1d)-1]>altustsinir[1]:
        resultMA=find_usdt_and_numbersMA15m(raw_text)
        longacMA=[]
        for c in resultMA:
            if binle(c[0]) in mysymbols3 and acabilirmiyim(binle(c[0])):
                if binle(c[0]) not in longacMA:
                    longacMA.append(binle(c[0]))
                    #print(longacMA)
        
        for coin in longacMA:
            if coin in mylonglarMA:
                print(f"{coin} zaten vardı")
            else:
                #mylonglarMA.append(coin)
                buy_position(coin, myleverage, get_my_cost(), "mylonglarMA")
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in mylonglarMA:
            if coin in longacMA:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarMA")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarMA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print(f"Longlar:{mylonglarMA}")
    else:
        print("io1d<altustsinir[1]")

def AnaFonkSDV(raw_text):
    matchesSDV = re.findall(patternSDV, raw_text)
    coin_listSDV = [match + "USDT" for match in matchesSDV]
    matchesSDV2 = re.findall(patternSDVtek, raw_text)
    coin_listSDV2 = [match + "USDT" for match in matchesSDV2]
    matchesSDV3 = re.findall(patternSDVasagicift, raw_text)
    coin_listSDV3 = [match + "USDT" for match in matchesSDV3]
    matchesSDV4 = re.findall(patternSDVasagitek, raw_text)
    coin_listSDV4 = [match + "USDT" for match in matchesSDV4]
    combined_list = coin_listSDV + coin_listSDV2
    combined_list2 = coin_listSDV3 + coin_listSDV4

    mylonglar=[]
    myshortlar=[]
    if check_arrowsIO(mytextio[0]) and io1d[len(io1d)-1]>altustsinir[1]: #len(combined_list) > 0: 
        mySDVlist=[]
        for coin in combined_list:
            if binle(coin) in mysymbols3 and acabilirmiyim(binle(coin)):
                mySDVlist.append(binle(coin))

        for coin in mySDVlist:
            if coin in mylonglarSDV:
                print(f"{coin} zaten vardı")
            else:
                #mylonglarSDV.append(coin)
                buy_position(coin, myleverage, mycost, "mylonglarSDV")
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in mylonglarSDV:
            if coin in mySDVlist:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarSDV")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarSDV.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        mylonglar=mylonglarSDV
    else:
        print("io1d<altustsinir[1]")

    if io1d[len(io1d)-1]<altustsinir[0] or io1d[len(io1d)-1]>altustsinir[1]:#1: #not check_arrowsIO(mytextio[0]) and io1d[len(io1d)-1]<altustsinir[0]: #len(combined_list2) > 0: 
        mySDVlist=[]
        for coin in combined_list2:
            if binle(coin) in mysymbols3 and acabilirmiyim(binle(coin)):
                mySDVlist.append(binle(coin))

        for coin in mySDVlist:
            if coin in myshortlarSDV:
                print(f"{coin} zaten vardı")
            else:
                #myshortlarSDV.append(coin)
                sell_position(coin, myleverage, mycost, "myshortlarSDV")
                print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in myshortlarSDV:
            if coin in mySDVlist:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin,"myshortlarSDV")
                print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarSDV.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        myshortlar=myshortlarSDV
    else:
        print("io1d altustsinir[0] ile altustsinir[1] arasında.")
    print(f"Shortlar:{myshortlar}")
    print(f"Longlar:{mylonglar}")

def AnaFonkCi(text):
    #if 1: #not check_arrowsIO(mytextio[0]):
    if "USDT" in text:
        cirawtext.clear()
        cirawtext.append(text)
    patternCiid5m = r'\b(\w+USDT)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+)\s+(\d+,\d+)'
    matchesCiid5m = re.findall(patternCiid5m, cirawtext[0])
    resultCiid5m = [[match[0], float(match[1].replace(',', '.')), float(match[2].replace(',', '.')), float(match[3]), float(match[4].replace(',', '.'))] for match in matchesCiid5m]
    #print(resultCiid5m)
    longAc=[]
    shortAc=[]
    for c in resultCiid5m:
        if binle(c[0]) in mysymbols3 and acabilirmiyim(binle(c[0])):
            if (((c[1]-c[2])>0.02) and c[1]>1 and c[2]<1) or ((c[1]-c[2])>0.05):
                if c[4]<6:
                    longAc.append(binle(c[0]))
            if (((c[2]-c[1])>0.02) and c[1]<1 and c[2]>1)or ((c[2]-c[1])>0.05):
                if c[4]>0.7:
                    shortAc.append(binle(c[0]))
    
    if False: #check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]>altustsinir[1]:
        for coin in longAc:
            if coin in mylonglarCi:
                print(f"{coin} zaten vardı")
            else:
                #mylonglarCi.append(coin)
                buy_position(coin, myleverage, mycost, "mylonglarCi")
                print(f"{coin} long açıldı")
                #await telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        for coin in mylonglarCi:
            if coin in longAc:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarCi")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarCi.remove(coin)
            #await telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")     
        if len(myshortlarCi)>0:
            for coin in myshortlarCi:
                close_position(coin,"myshortlarCi")
                print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarCi.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")  
    else:
        print("io1d<altustsinir[1]") 
    
    if cift_ema_sinyal(io1d)[1] and io1d[-1]!=49.9 and io1d[-1]!=50 and io1d[-1]!=50.1:#ortalamayagorepozisyonacayimmi("short"): #not is_above_last_period_average(io1d[-1],io1d,smaperiod): #not check_arrowsIO(mytextio[0]) and io1d[len(io1d)-1]<altustsinir[0]:
        for coin in shortAc:
            if coin in myshortlarCi:
                print(f"{coin} zaten vardı")
            else:
                #myshortlarCi.append(coin)
                sell_position(coin, myleverage, get_my_cost(), "myshortlarCi")
                print(f"{coin} short açıldı")
                #await telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        """
        for coin in myshortlarCi:
            if coin in shortAc:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin,"myshortlarCi")
                print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarCi.remove(coin)
                #await telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        
        if len(mylonglarCi)>0:
            for coin in mylonglarCi:
                close_position(coin,"mylonglarCi")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarCi.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")   
        """
    else:
        print("io1d>altustsinir[0]")
    print(f"Shortlar:{myshortlarCi}")
    print(f"Longlar:{mylonglarCi}")
    
def AnaFonkIOF(raw_text):
    #OXTUSDT 7,0X Payı:%3,7 Pahalılık:8,0 🔼🔻🔻🔼🔼 Grafik (http://tradingview.com/chart/?symbol=BINANCE:OXTUSDT)
    #['TIAUSDT', 0.4, 0.9, 1.9, [True, True, True, False, True]]
    parsed_data = parse_usdt_dataIOF(raw_text)
    if io1d[-1]>50.1 and (extract_market_buying_power(mytextio[0])>1 or cift_ema_sinyal(iopower)[0]):#False: #is_above_last_period_average(io1d[-1],io1d,smaperiod): #False: #not is_above_last_period_average(io1d[-1],io1d,smaperiod): #check_arrowsIO(mytextio[0])  and io1d[-1]>altustsinir[1]:
        longAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]>1.2 and entry[2]>0.5 and entry[3]<2 and entry[4][0] and entry[4][1] and entry[4][2] and entry[4][3] and entry[4][4]:
                longAc.append(binle(entry[0]))
        print(f"longAc: {longAc}")
        for coin in longAc:
            if coin in mylonglarIOF:
                print(f"{coin} zaten vardı")
            elif coin in yasaklilist:
                print(f"Açılamayan coin: {coin}")
            else:
                if True:#check_arrowsIO(mytextio[0]):
                    #mylonglarIOF.append(coin)
                    buy_position(coin, myleverage, get_my_cost(), "mylonglarIOF")
                    print(f"{coin} long açıldı")
        """
        for coin in mylonglarIOF:
            if coin in longAc:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarIOF")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarIOF.remove(coin)
        """
    else:
        print("io1d<altustsinir[1]")
        
    if io1d[-1]<49.9: # and (extract_market_buying_power(mytextio[0])<1):#not is_above_last_period_average(io1d[-1],io1d,smaperiod): # and not io15m1h4hyuksektemi(): #not check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]<altustsinir[0]: #len(combined_list2) > 0: 
        #OXTUSDT 7,0X Payı:%3,7 Pahalılık:8,0 🔼🔻🔻🔼🔼 Grafik (http://tradingview.com/chart/?symbol=BINANCE:OXTUSDT)
        #['TIAUSDT', 0.4, 0.9, 1.9, [True, True, True, False, True]]
        shortAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and not entry[4][0] and not entry[4][1] and not entry[4][2] and not entry[4][3] and not entry[4][4]:
                shortAc.append(binle(entry[0]))
        print(shortAc)
        for coin in shortAc:
            if coin in myshortlarIOF:
                print(f"{coin} zaten vardı")
            elif coin in yasaklilist:
                print(f"Açılamayan coin: {coin}")
            else:
                #myshortlarIOF.append(coin)
                sell_position(coin, myleverage, get_my_cost(), "myshortlarIOF")
                print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        """
        for coin in myshortlarIOF:
            if coin in shortAc:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin,"myshortlarIOF")
                print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarIOF.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        """
    else:
        print("io1d>altustsinir[0]")
    print(f"Longlar:{mylonglarIOF}")
    print(f"Shortlar:{myshortlarIOF}")
    
################################# Ana Fonksiyon

async def main():
    global calissinmi
    await telegram_client.start(phone=phone_number)
    @telegram_client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi:\n {event.raw_text}')

        if event.raw_text.startswith("Marketteki Tüm Coinlere Olan Nakit Girişi Raporu"): #IO
            AnaFonkIO(event.raw_text)

        if event.raw_text.startswith("Canlı olan coin sayısı") and check_arrowsIO(mytextio[0]): #KA
            AnaFonkKA(event.raw_text)

        if event.raw_text.startswith("?????Yapay zeka,") and check_arrowsIO(mytextio[0]): #Marketanaliz MA
            AnaFonkMA(event.raw_text)
        
        if event.raw_text.startswith("????????Korelasyon Şiddeti Raporu (5m)"): #ci i d 5m
            AnaFonkCi(event.raw_text)

        if event.raw_text.startswith("??????Sert Hareket Edenler"): #SDV
            AnaFonkSDV(event.raw_text)     

        if event.raw_text.startswith("?????????Marketteki Tüm Coinlere Olan en çok nakit girişi olanlar."): #IOF
            AnaFonkIOF(event.raw_text)   
        
    while True:
        if True:
            komutlar=["iof","ssr","marketanaliz","ci s d 5m","acc","grio","dayhigh","p btc","ap","sdv"]
            mysent49=["sdv","marketanaliz","io","ci i d 5m","ka","iof"]
            mysent4849=["nls io xxx++","nls io xxxx+","nls io xx+++","nls io x++++","nls io x+++", "p btc","p btc","p btc","p btc","p btc","p btc","p btc","p btc"]
            mysent48=["sdv","ci i d 5m","iof"]
            iokaiof=["io","ka","iof", "io"]
            iokaci=["io","ka","ci i d 5m", "io"]
            ciio=["ci i d 5m","io"]
            kaio=["ka","io"]
            iofio=["iof","io"]
            kaio=["ka","io"]
            random.shuffle(kaio)
            random.shuffle(mysent48)
            random.shuffle(iokaiof)
            random.shuffle(kaio)
            random.shuffle(iofio)
            random.shuffle(ciio)
            random.shuffle(iokaci)
            if mymesaj:
                for mesaj in mymesaj:
                    await mesajgonder(f"Otomatik kapatılan coinler: {mesaj}",alert_user)
                mymesaj.clear()
            while True:
                if calissinmi:
                    await telegram_client.send_message(target_user, komutlar[rastgele_sayi(0,len(komutlar)-1)])
                    await asyncio.sleep(rastgele_sayi(15,45))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
                    break
                else:
                    await asyncio.sleep(rastgele_sayi(10,20))
            while True:
                if calissinmi:
                    await telegram_client.send_message(target_user, kaio[0]) #mysent[rastgele_komut()] )#'marketanaliz')
                    await asyncio.sleep(rastgele_sayi(35,100))
                    break
                else:
                    await asyncio.sleep(rastgele_sayi(10,20))
            while True:
                if calissinmi:
                    await telegram_client.send_message(target_user, kaio[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                    await asyncio.sleep(rastgele_sayi(35,100))
                    break
                else:
                    await asyncio.sleep(rastgele_sayi(10,20))
            
            
            await asyncio.sleep(rastgele_sayi(15,30))
            if False: #acmakapamalistesi:
                #await telegram_client.send_message(alert_user, acmakapamalistesi)
                acmakapamalistesi.clear()
        
        elif io1d[len(io1d)-1]>altustsinir[0] and io1d[len(io1d)-1]<altustsinir[1]:
            random.shuffle(mysent4849)
            await telegram_client.send_message(target_user, "io") #komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(20,50))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            if io1d[len(io1d)-1]>altustsinir[1] or io1d[len(io1d)-1]<altustsinir[0]:
                await telegram_client.send_message(target_user, "io") #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(50,100))
            else:
                await telegram_client.send_message(target_user, mysent4849[0]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(3000,5500))
        
        elif io1d[len(io1d)-1]>altustsinir[1]:
            random.shuffle(mysent49)
            await telegram_client.send_message(target_user, komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(100,200))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            await telegram_client.send_message(target_user, mysent49[0]) #mysent[rastgele_komut()] )#'marketanaliz')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
            await telegram_client.send_message(target_user, mysent49[2]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
            await telegram_client.send_message(target_user, mysent49[3]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
            await telegram_client.send_message(target_user, mysent49[4]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[5]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
        

with telegram_client:
    telegram_client.loop.run_until_complete(main())