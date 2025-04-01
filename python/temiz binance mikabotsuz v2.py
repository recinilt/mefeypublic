from telethon import TelegramClient, events
from binance.client import Client
import asyncio
import re
import random
import time
from binance.enums import *
import requests
import json

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


################################################## Değişkeler:
#binance future listesi
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
mycost=1
myleverage=11
komutlar=["io","io","io","io","io","io","io","io","io","io","io","io","io","io","io","io","io","iof","ssr","marketanaliz","ka","ci s d 5m","acc","grio","dayhigh","p btc","ap","io","sdv"]
kactanbuyuk=17
mysent49=["sdv","marketanaliz","io","ci i d 5m","ka","iof"]
mysent4849=["nls io xxx++","nls io xxxx+","nls io xx+++","nls io x++++","nls io x+++", "p btc","p btc","p btc","p btc","p btc","p btc","p btc","p btc"]
mysent48=["sdv","ci i d 5m","iof"]
iokaiof=["io","ka","iof", "io"]
iokaci=["io","ka","ci i d 5m", "io"]
ciio=["ci i d 5m","io"]
kaio=["ka","io"]
iofio=["iof","io"]
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
#ilkio=float(input("io rakamını giriniz:"))
#ilkkackez=int(input("kaç tane io eklensin?"))
#for i in range(1, ilkkackez + 1):
    #print(i)
#    io1d.append(ilkio)
cirawtext=[]
acmakapamalistesi=[]
symbolsprices=[]
piyasatoplamprices=[]
symbolsvolumes=[]
symbolspricesvolumespercentages=[] #  [[coin, [price, volume, volumepercentage]],[coin, [price, volume, volumepercentage]]]

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

def get_volume(symbol):
    try:
        ticker = binanceclient.get_symbol_ticker(symbol=symbol.upper())
        return ticker['quoteVolume']
    except Exception as e:
        print(f"Error: {e}")
        return 1

def symbolpricesidoldur():
    print("ilk dolduruş")
    """
    volumeler=[]
    for coin in mysymbols3:
        volume=get_volume(coin)
        symbolsprices.append([coin,volume])
        volumeler.append(volume)
    toplamvolume=sum(volumeler)
    for c in symbolsprices:
        c.append(c[1]/toplamvolume)
    print(symbolsprices)
    """

def doldurus(kacinci): 
    if kacinci=="ilk": # [coin, [price, volume, volumepercentage]]
        # Futures tüm işlem çiftlerini almak
        tickers = binanceclient.futures_ticker()
        # USDT çiftlerini filtrele ve hacimleri al
        prices=[]
        usdt_pairs = []
        total_volume = 0
        for ticker in tickers:
            symbol = ticker['symbol']
            if symbol.endswith("USDT"):  # Sadece USDT çiftlerini seç
                volume = round(float(ticker['volume']),2)  # Hacmi float olarak al
                price=float(ticker['lastPrice'])
                prices.append(price)
                usdt_pairs.append([symbol, [price,volume]])
                total_volume += volume  # Toplam hacmi hesapla
        # Her bir coin için hacim oranını hesapla ve ekle
        for pair in usdt_pairs:
            coin = pair[0]  # Coin ismi (USDT'li şekilde)
            volume = pair[1][1]  # Hacmi
            percentage = round(((volume / total_volume) * 100),1)  # Hacmin toplam hacme oranı
            pair[1].append(percentage)  # Oranı listeye ekle
        piyasatoplamprices.append(sum(prices))
        # Sonuçları yazdır
        return usdt_pairs
    elif kacinci=="sonraki": #[[coin, [price, volume, volumepercentage]],[coin, [price, volume, volumepercentage]]]
        # Futures tüm işlem çiftlerini almak
        tickers = binanceclient.futures_ticker()
        # USDT çiftlerini filtrele ve hacimleri al
        #usdt_pairs = []
        prices=[]
        myvolume=[]
        total_volume = 0
        for ticker in tickers:
            symbol = ticker['symbol']
            if symbol.endswith("USDT"):  # Sadece USDT çiftlerini seç
                volume = round(float(ticker['volume']),2)  # Hacmi float olarak al
                price=float(ticker['lastPrice'])
                prices.append(price)
                myvolume.append([symbol,volume,price])
                total_volume += volume  # Toplam hacmi hesapla
        # Her bir coin için hacim oranını hesapla ve ekle
        for c in symbolspricesvolumespercentages:
            for cift in myvolume:
                if c[0]==myvolume[0]:
                    percentage = round(((myvolume[1] / total_volume) * 100),1)  # Hacmin toplam hacme oranı
                    c.append([myvolume[2],myvolume[1],percentage])
                    break
        print("oranlar eklendi")
        piyasatoplamprices.append(sum(prices))

        

symbolspricesvolumespercentages=doldurus("ilk")

def myquantity(coin):
    return round(((mycost*myleverage)/float(get_price(coin))),3)

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


def close_position(coin,liste):
    # Mevcut pozisyonu kapat
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
            mtext=f"Kapatılan Çift: {position['symbol']}, Miktar: {position['positionAmt']}, Giriş Fiyatı: {position['entryPrice']}, Çıkış fiyatı: {get_price(position["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            hesapla(coin, side, myquantity)
            eklesil(coin,liste,"sil")
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

def closelongs():
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
            mtext=f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}, Çıkış fiyatı: {get_price(pos["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            time.sleep(7)  # 5 saniye bekle
    #return myacikusdtlist

def closeshorts():
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
            mtext=f"Kapatılan Çift: {pos['symbol']}, Miktar: {pos['positionAmt']}, Giriş Fiyatı: {pos['entryPrice']}, Çıkış fiyatı: {get_price(pos["symbol"])}"
            acmakapamalistesi.append(mtext)
            print(mtext)
            time.sleep(7)  # 5 saniye bekle
    #return myacikusdtlist

    
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
# Ana fonksiyondakiler:
def AnaFonkIO(raw_text):
    mytextio.clear()
    mytextio.append(raw_text)
    io1d.append(convert_to_floatIO(mytextio[0]))
    if is_above_last_period_average(io1d[-1],io1d,smaperiod):
        IOcikiyorsakapat() #shortlar kapanacak
    if not is_above_last_period_average(io1d[-1],io1d,smaperiod):
        IOdusuyorsakapat() #longlar kapanacak
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
    print(f"IO 1d, yukarı trendde mi?: {is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod)}")
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

def AnaFonkKA(raw_text):
    #[1,???], ['ETHUSDT', 1.2, 1.1, 1.048, 788, True, 7.3]
    #TRX TS:1,6 MTS:1,4 PT:1,048 Dk:288✅ Kar:%7,6 😍 Grafik (http://tradingview.com/chart/?symbol=BINANCE:TRXUSDT)

    result = extract_coin_dataKA(raw_text)
    #print(result)
    if result[0][0]>-1 and ortalamayagorepozisyonacayimmi("long"): # and not io15m1h4hdusuktemi():
        myFKAlist=[]
        kadakilonglar=[]
        for coin in result:
            print(coin[0], coin[2],coin[3],coin[5],coin[6])
            if binle(coin[0]) in mysymbols3 and coin[2]<2.5 and coin[2]>1.1 and coin[3]>1.01 and coin[5]==True and coin[6]<15 and acabilirmiyim(binle(coin[0])):
                myFKAlist.append(binle(coin[0]))
            if binle(coin[0]) in mysymbols3:
                kadakilonglar.append(binle(coin[0]))
        
        for coin in myFKAlist:
            if coin in mylonglarKA:
                print(f"{coin} zaten vardı")
            else:
                #mylonglarKA.append(coin)
                buy_position(coin, myleverage, mycost, "mylonglarKA")
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
                buy_position(coin, myleverage, mycost, "mylonglarMA")
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
    
    if ortalamayagorepozisyonacayimmi("short"): #not is_above_last_period_average(io1d[-1],io1d,smaperiod): #not check_arrowsIO(mytextio[0]) and io1d[len(io1d)-1]<altustsinir[0]:
        for coin in shortAc:
            if coin in myshortlarCi:
                print(f"{coin} zaten vardı")
            else:
                #myshortlarCi.append(coin)
                sell_position(coin, myleverage, mycost, "myshortlarCi")
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
    if False: #is_above_last_period_average(io1d[-1],io1d,smaperiod): #False: #not is_above_last_period_average(io1d[-1],io1d,smaperiod): #check_arrowsIO(mytextio[0])  and io1d[-1]>altustsinir[1]:
        longAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]>1 and entry[2]>0.5 and entry[3]<2 and entry[4][0] and entry[4][1] and entry[4][2] and entry[4][3]:
                longAc.append(binle(entry[0]))

        for coin in longAc:
            if coin in mylonglarIOF:
                print(f"{coin} zaten vardı")
            else:
                if check_arrowsIO(mytextio[0]):
                    #mylonglarIOF.append(coin)
                    buy_position(coin, myleverage, mycost, "mylonglarIOF")
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
        
    if not is_above_last_period_average(io1d[-1],io1d,smaperiod): # and not io15m1h4hyuksektemi(): #not check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]<altustsinir[0]: #len(combined_list2) > 0: 
        #OXTUSDT 7,0X Payı:%3,7 Pahalılık:8,0 🔼🔻🔻🔼🔼 Grafik (http://tradingview.com/chart/?symbol=BINANCE:OXTUSDT)
        #['TIAUSDT', 0.4, 0.9, 1.9, [True, True, True, False, True]]
        shortAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and not entry[4][0] and not entry[4][1] and not entry[4][2] and not entry[4][3]:
                shortAc.append(binle(entry[0]))
        print(shortAc)
        for coin in shortAc:
            if coin in myshortlarIOF:
                print(f"{coin} zaten vardı")
            else:
                #myshortlarIOF.append(coin)
                sell_position(coin, myleverage, mycost, "myshortlarIOF")
                print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in myshortlarIOF:
            if coin in shortAc:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin,"myshortlarIOF")
                print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarIOF.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
    else:
        print("io1d>altustsinir[0]")
    print(f"Longlar:{mylonglarIOF}")
    print(f"Shortlar:{myshortlarIOF}")
    
################################# Ana Fonksiyon
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
myemapreirodkisa=14
myemapreiroduzun=25

def piyasayukselistemiv2():
    if len(piyasatoplamprices)>=smaperiod:

def piyasayukselistemi():
    if len(piyasatoplamprices)>=smaperiod:
        # Son 7 elemanı al
        last_smaperiod = piyasatoplamprices[(-1 * smaperiod):]
        # Son 7 elemanın ortalamasını hesapla
        average = sum(last_smaperiod) / len(last_smaperiod) if last_smaperiod else piyasatoplamprices[-1]
        # Sayı ortalamadan büyükse True, değilse False döndür
        if piyasatoplamprices[-1] > average:
            print("piyasa yükselişte")
        else:
            print("piyasa düşüşte")
        return piyasatoplamprices[-1] > average
    else:
        print("yeterli veri yok")
        return False

def hangicoinleryukseliste():
    if piyasayukselistemi():
        yukselistekiler=[]
        for coinlistesi in symbolspricesvolumespercentages: #  [[coin, [price, volume, volumepercentage],[price, volume, volumepercentage],[price, volume, volumepercentage]],[coin, [price, volume, volumepercentage],[price, volume, volumepercentage],[price, volume, volumepercentage]]]
            myprices=[]
            for price in coinlistesi:
                if "USDT" in price:
                    continue
                else:
                    myprices.append(price[0])
            if is_above_last_period_average(myprices[-1],myprices,smaperiod):
                if coinlistesi[-1][-1]>0.5:
                    yukselistekiler.append(coinlistesi[0])
        return yukselistekiler
        
    else:
        return []

def main():
    while True:
        doldurus("sonraki")
        if piyasayukselistemi():
            yukselistekiler=hangicoinleryukseliste()
            for coin in yukselistekiler:
                buy_position(coin, myleverage, mycost, "mylonglarKA")
        else:
            closelongs()
        
        
        print(piyasatoplamprices)
        print(len(mysymbols3))

        time.sleep(180)
        
main()

"""
    await telegram_client.start(phone=phone_number)
    @telegram_client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi:\n {event.raw_text}')

        

        if event.raw_text.startswith("?????Marketteki Tüm Coinlere Olan Nakit Girişi Raporu"): #IO
            AnaFonkIO(event.raw_text)

        if event.raw_text.startswith("???????Canlı olan coin sayısı") and check_arrowsIO(mytextio[0]): #KA
            AnaFonkKA(event.raw_text)

        if event.raw_text.startswith("?????Yapay zeka,") and check_arrowsIO(mytextio[0]): #Marketanaliz MA
            AnaFonkMA(event.raw_text)
        
        if event.raw_text.startswith("??????Korelasyon Şiddeti Raporu (5m)"): #ci i d 5m
            AnaFonkCi(event.raw_text)

        if event.raw_text.startswith("??????Sert Hareket Edenler"): #SDV
            AnaFonkSDV(event.raw_text)     

        if event.raw_text.startswith("???????Marketteki Tüm Coinlere Olan en çok nakit girişi olanlar."): #IOF
            AnaFonkIOF(event.raw_text)   

    while True:
        doldurus("sonraki")
        if piyasayukselistemi():
            yukselistekiler=hangicoinleryukseliste()
            for coin in yukselistekiler:
                buy_position(coin, myleverage, mycost, "mylonglarKA")
        else:
            closelongs()
        
        
        print(piyasatoplamprices)
        print(len(mysymbols3))
        

        await asyncio.sleep(180)
        if False:
            random.shuffle(mysent48)
            random.shuffle(iokaiof)
            random.shuffle(kaio)
            random.shuffle(iofio)
            random.shuffle(ciio)
            random.shuffle(iokaci)
            await telegram_client.send_message(target_user, komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(35,100))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            if is_above_last_period_average(io1d[-1],io1d,smaperiod):
                await telegram_client.send_message(target_user, kaio[0]) #mysent[rastgele_komut()] )#'marketanaliz')
                await asyncio.sleep(rastgele_sayi(35,100))
                await telegram_client.send_message(target_user, kaio[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(35,150))
            else:
                await telegram_client.send_message(target_user, ciio[0]) #mysent[rastgele_komut()] )#'marketanaliz')
                await asyncio.sleep(rastgele_sayi(35,100))
                await telegram_client.send_message(target_user, ciio[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(35,150))
            await telegram_client.send_message(target_user, iokaci[0]) #mysent[rastgele_komut()] )#'marketanaliz')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, iokaci[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,150))
            await telegram_client.send_message(target_user, iokaci[2]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, iokaci[3]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent48[0]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
            if acmakapamalistesi:
                await telegram_client.send_message(alert_user, acmakapamalistesi)
                acmakapamalistesi.clear()
        
        elif False: #io1d[len(io1d)-1]>altustsinir[0] and io1d[len(io1d)-1]<altustsinir[1]:
            random.shuffle(mysent4849)
            await telegram_client.send_message(target_user, "io") #komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(20,50))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            if io1d[len(io1d)-1]>altustsinir[1] or io1d[len(io1d)-1]<altustsinir[0]:
                await telegram_client.send_message(target_user, "io") #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(50,100))
            else:
                await telegram_client.send_message(target_user, mysent4849[0]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(3000,5500))
        
        elif False: #io1d[len(io1d)-1]>altustsinir[1]:
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
    """

#with telegram_client:
#    telegram_client.loop.run_until_complete(main())