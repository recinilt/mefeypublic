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
mysent48=["sdv","io","ci i d 5m","iof"]
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
smaperiod=-3
myacclongdevammi=[["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1]]
myaccshortdevammi=[["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],["BTCUSDT",1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1]]
mylonglarACC=[]
myshortlarACC=[]
myacccoinlerlong=[["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1]]
myacccoinlershort=[["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1],["BTCUSDT",1.1]]


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
    coin_count2=[coin_count,0]

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
    return round(((mycost*myleverage)/float(get_price(coin))),3)

def close_position(coin,liste):
    # Mevcut pozisyonu kapat
    positions = binanceclient.futures_position_information(symbol=coin)
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            myquantity=abs(float(position['positionAmt']))
            order = binanceclient.futures_create_order(
                symbol=coin,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=myquantity
            )
            print(f"Pozisyon kapatıldı: {order}")
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
    if is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
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
    if not is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
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
    return num > average


def eklesil(coin, liste, eylem):
    if eylem=="ekle":
        if liste=="mylonglarKA":
            mylonglarKA.append(coin)
        elif liste=="mylonglarSDV":
            mylonglarSDV.append(coin)
        elif liste=="mylonglarMA":
            mylonglarMA.append(coin)
        elif liste=="mylonglarIOF":
            mylonglarIOF.append(coin)
        elif liste=="mylonglarCi":
            mylonglarCi.append(coin)
        elif liste=="mylonglarACC":
            mylonglarACC.append(coin)
        elif liste=="myshortlarSDV":
            myshortlarSDV.append(coin)
        elif liste=="myshortlarCi":
            myshortlarCi.append(coin)
        elif liste=="myshortlarIOF":
            myshortlarIOF.append(coin)
        elif liste=="myshortlarACC":
            myshortlarACC.append(coin)
    if eylem=="sil":
        if liste=="mylonglarKA":
            mylonglarKA.remove(coin)
        elif liste=="mylonglarSDV":
            mylonglarSDV.remove(coin)
        elif liste=="mylonglarMA":
            mylonglarMA.remove(coin)
        elif liste=="mylonglarIOF":
            mylonglarIOF.remove(coin)
        elif liste=="mylonglarCi":
            mylonglarCi.remove(coin)
        elif liste=="mylonglarACC":
            mylonglarACC.append(coin)
        elif liste=="myshortlarSDV":
            myshortlarSDV.remove(coin)
        elif liste=="myshortlarCi":
            myshortlarCi.remove(coin)
        elif liste=="myshortlarIOF":
            myshortlarIOF.remove(coin)
        elif liste=="myshortlarACC":
            myshortlarACC.remove(coin)

def usdt_veri_islemeACC(metin):
    #XLMUSDT 0,5059 17,1 2,01 0,24 + + + + + 1,86
    #[['XLMUSDT', [0.5059, 17.1, 2.01, 0.24], [True, True, True, True, True], 1.86]
    pattern = re.compile(r"(\w+USDT)\s([\d,]+)\s([\d,]+)\s([\d,]+)\s([\d,]+)\s([\+\-])\s([\+\-])\s([\+\-])\s([\+\-])\s([\+\-])\s([\d,]+)")
    matches = pattern.findall(metin)

    result = []

    for match in matches:
        coin = match[0]
        numbers = [float(num.replace(",", ".")) for num in match[1:5]]
        trend = [True if t == "+" else False for t in match[5:10]]
        score = float(match[10].replace(",", "."))
        result.append([coin, numbers, trend, score])

    return result

# Ana fonksiyondakiler:
def AnaFonkIO(raw_text):
    mytextio.clear()
    mytextio.append(raw_text)
    io1d.append(convert_to_floatIO(mytextio[0]))
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
    if result[0][0]>-1 and io1d[len(io1d)-1]>altustsinir[1]:
        myFKAlist=[]
        kadakilonglar=[]
        for coin in result:
            if binle(coin[0]) in mysymbols3 and coin[2]<2 and coin[3]>1.03 and coin[5]==True and coin[6]<10 and acabilirmiyim(binle(coin)):
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
        
        for coin in mylonglarKA:
            if coin in kadakilonglar:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarKA")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarKA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print(f"Longlar:{mylonglarKA}")
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
    patternCiid5m = r'\b(\w+USDT)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+)\s+(\d+,\d+)'
    matchesCiid5m = re.findall(patternCiid5m, text)
    resultCiid5m = [[match[0], float(match[1].replace(',', '.')), float(match[2].replace(',', '.')), float(match[3]), float(match[4].replace(',', '.'))] for match in matchesCiid5m]
    longAc=[]
    shortAc=[]
    for c in resultCiid5m:
        if binle(c[0]) in mysymbols3 and acabilirmiyim(binle(c[0])):
            if ((c[1]-c[2]>0.02) and c[1]>1 and c[2]<1) or (c[1]-c[2]>0.10):
                if c[4]<6:
                    longAc.append(binle(c[0]))
            if ((c[2]-c[1]>0.02) and c[1]<1 and c[2]>1)or (c[2]-c[1]>0.10):
                if c[4]>0.7:
                    shortAc.append(binle(c[0]))
    
    if check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]>altustsinir[1]:
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
    
    if not check_arrowsIO(mytextio[0]) and io1d[len(io1d)-1]<altustsinir[0]:
        for coin in shortAc:
            if coin in myshortlarCi:
                print(f"{coin} zaten vardı")
            else:
                #myshortlarCi.append(coin)
                sell_position(coin, myleverage, mycost, "myshortlarCi")
                print(f"{coin} short açıldı")
                #await telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
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
    else:
        print("io1d>altustsinir[0]")
    print(f"Shortlar:{myshortlarCi}")
    print(f"Longlar:{mylonglarCi}")
    
def AnaFonkIOF(raw_text):
    #OXTUSDT 7,0X Payı:%3,7 Pahalılık:8,0 🔼🔻🔻🔼🔼 Grafik (http://tradingview.com/chart/?symbol=BINANCE:OXTUSDT)
    #['TIAUSDT', 0.4, 0.9, 1.9, [True, True, True, False, True]]
    
    parsed_data = parse_usdt_dataIOF(raw_text)
    if check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]>altustsinir[1]:
        longAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]>1 and entry[2]>0.5 and entry[3]<5 and entry[4][0] and entry[4][1] and entry[4][2] and entry[4][3]:
                longAc.append(binle(entry[0]))

        for coin in longAc:
            if coin in mylonglarIOF:
                print(f"{coin} zaten vardı")
            else:
                if check_arrowsIO(mytextio[0]):
                    #mylonglarIOF.append(coin)
                    buy_position(coin, myleverage, mycost, "mylonglarIOF")
                    print(f"{coin} long açıldı")
        
        for coin in mylonglarIOF:
            if coin in longAc:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin,"mylonglarIOF")
                print(f"{coin} pozisyonu kapatıldı.")
                #mylonglarIOF.remove(coin)
    else:
        print("io1d<altustsinir[1]")
        
    if not check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]<altustsinir[0]: #len(combined_list2) > 0: 
        shortAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]<1.7 and entry[2]>0.5 and entry[3]>0.5 and not entry[4][0] and not entry[4][1] and not entry[4][2] and not entry[4][3] and not entry[4][4]:
                shortAc.append(binle(entry[0]))

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

def AnaFonkACC(raw_text):
    #XLMUSDT 0,5059 17,1 2,01 0,24 + + + + + 1,86
    #[['XLMUSDT', [0.5059, 17.1, 2.01, 0.24], [True, True, True, True, True], 1.86]
    
    parsed_data = usdt_veri_islemeACC(raw_text)
    if 1:
        longAc=[]
        for entry in parsed_data:
            myacclongacsymbol.append(binle(entry[0]))
            myacclongac.append([binle(entry[0]),entry[1][1]])
            #print(f"myacclongacsymbol {myacclongac}")
            if binle(entry[0]) in mysymbols3 : #and acabilirmiyim(binle(entry[0])) and entry[1]>1 and entry[2]>0.5 and entry[3]<5 and entry[4][0] and entry[4][1] and entry[4][2] and entry[4][3]:
                if entry[1][1]>2 and entry[2][0] and entry[2][1] and entry[2][2] and entry[2][3] and entry[2][4]:
                    longAc.append(binle(entry[0]))
                    #accdevammilistesiekle([entry[0],entry[1][1]],"long")
            #print(f"myacclongacsymbol: {myacclongacsymbol}")     
            #print(f"myacclongac: {myacclongac}")  
        if 1:
            for coin in longAc: # mylongac[0][1] mylongac[0][0][0]  c[1] c[0][0]
                if coin in mylonglarACC:
                    print(f"{coin} zaten vardı")
                else:
                    if ACCopendevammi2(coin, "long"): #check_arrowsIO(mytextio[0]):
                        #mylonglarIOF.append(coin)
                        buy_positionACC(coin, myleverage, mycost, "mylonglarACC")
                        #print(f"{coin} long açıldı")
            
            for coin in mylonglarACC:
                if coin in longAc:
                    if ACCopendevammi2(coin, "long"):
                        print(f"{coin} 'e zaten long açılmış.")
                    else:
                        close_position(coin,"mylonglarACC")
                else:
                    close_position(coin,"mylonglarACC")
                    #print(f"{coin} pozisyonu kapatıldı.")
                    #mylonglarIOF.remove(coin)
    else:
        print("io1d<altustsinir[1]")
        
    if True: #not check_arrowsIO(mytextio[0])  and io1d[len(io1d)-1]<altustsinir[0]: #len(combined_list2) > 0: 
        shortAc=[]
        for entry in parsed_data:
            myaccshortacsymbol.append(binle(entry[0]))
            myaccshortac.append([binle(entry[0]),entry[1][1]])
            #print(myaccshortacsymbol)
            if binle(entry[0]) in mysymbols3: # and acabilirmiyim(binle(entry[0])) and entry[1]<1.7 and entry[2]>0.5 and entry[3]>0.5 and not entry[4][0] and not entry[4][1] and not entry[4][2] and not entry[4][3] and not entry[4][4]:
                if entry[1][1]<-2 and not entry[2][0] and not entry[2][1] and not entry[2][2] and not entry[2][3] and not entry[2][4]:
                    shortAc.append(binle(entry[0]))
                    #accdevammilistesiekle([entry[0],entry[1][1]],"short")
                    

        for coin in shortAc:
            if coin in myshortlarACC:
                print(f"{coin} zaten vardı")
            elif ACCopendevammi2(coin, "short"):
                #myshortlarIOF.append(coin)
                sell_positionACC(coin, myleverage, mycost, "myshortlarACC")
                #print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in myshortlarACC:
            if coin in shortAc:
                if ACCopendevammi2(coin, "short"):
                    print(f"{coin} 'e zaten short açılmış.")
                else:
                    close_position(coin,"myshortlarACC")
            else:
                close_position(coin,"myshortlarACC")
                #print(f"{coin} pozisyonu kapatıldı.")
                #myshortlarIOF.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
    else:
        print("io1d>altustsinir[0]")
    #ACCopendevammi()
    #print(f"Longlar:{mylonglarIOF}")
    #print(f"Shortlar:{myshortlarIOF}")
    #ACCkontrol()
    #print(myacclongac)
    #print(myacclongacsymbol)
    #print(mylonglarACC)
    #print(myshortlarACC)
    
def ACCkontrol():
    for c in mylonglarACC:
        if not ACCopendevammi2(c,"long"):
            close_position(c,"mylonglarACC")
    for c in myshortlarACC:
        if not ACCopendevammi2(c,"short"):
            close_position(c,"myshortlarACC")
    

"""
def is_above_last_period_averageACC(num, lst, period):
    # Son 7 elemanı al
    #period=3
    last_7 = lst[-3:]
    # Son 7 elemanın ortalamasını hesapla
    average = sum(last_7) / len(last_7) if last_7 else 49.1
    # Sayı ortalamadan büyükse True, değilse False döndür
    if average==49.1:
        return 49.1
    else:
        return num > average
"""
myacclongac=[]
myacclongacsymbol=[]
myaccshortac=[]
myaccshortacsymbol=[]

def ACCopendevammi2(coin,pozisyon):
    if pozisyon=="long":
        liste=[]
        if coin in myacclongacsymbol:
            for c in myacclongac:
                if c[0]==coin:
                    liste.append(c[1])
        mylist = liste[smaperiod:]
        print(mylist)
        average = sum(mylist) / len(mylist) if mylist else 1
        # Sayı ortalamadan büyükse True, değilse False döndür
        #if average==49.1:
        #    return False
        #else:
        print(mylist[-1] >= average)
        return mylist[-1] >= average
    elif pozisyon=="short":
        liste=[]
        if coin in myaccshortacsymbol:
            for c in myaccshortac:
                if c[0]==coin:
                    liste.append(c[1])
        mylist = liste[smaperiod:]
        average = sum(mylist) / len(mylist) if mylist else 100
        # Sayı ortalamadan büyükse True, değilse False döndür
        print(mylist[-1] < average)
        return mylist[-1] < average
    else:
        return True

            
def buy_positionACC(symbol, leverage, amount, liste):
    if not symbol in mylonglarACC:
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

def sell_positionACC(symbol, leverage, amount, liste):
    if not symbol in myshortlarACC:
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
     
    
"""
def ACCopendevammi(liste="surekli", pozisyon="surekli"):
    #LİSTE=LONGAC VEYA SHORTAC
    #POZİSYON=LONG VEYA SHORT
    #XLMUSDT 0,5059 17,1 2,01 0,24 + + + + + 1,86
    #[['XLMUSDT', [0.5059, 17.1, 2.01, 0.24], [True, True, True, True, True], 1.86]
    #is_above_last_period_average(num, lst, period)
    last_7 = lst[-3:]
    # Son 7 elemanın ortalamasını hesapla
    average = sum(last_7) / len(last_7) if last_7 else 49.1
    # Sayı ortalamadan büyükse True, değilse False döndür
    if average==49.1:
        return 49.1
    else:
        return num > average
    
    if pozisyon=="long":
        for c in liste:
            for coin in myacclongdevammi:
                if coin[0]==c:
                    if not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        if is_above_last_period_averageACC(coin[len(coin)-1], coin, 3):
                            print(f"devam {c}")
                            return True  
                        elif not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3): # and not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                            close_position(c,"mylonglarACC")
                            print(f"{c} pozisyonu kapatıldı.")
                            return False
    elif pozisyon=="short":
        for c in liste:
            for coin in myaccshortdevammi:
                if coin[0]==c:
                    if not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        if not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3):
                            print(f"devam {c}")
                            return True  
                        elif is_above_last_period_averageACC(coin[len(coin)-1], coin, 3):
                            close_position(c,"myshortlarACC")
                            print(f"{c} pozisyonu kapatıldı.")
                            return False
    else:
        return False
    if pozisyon=="surekli":
        for c in mylonglarACC:
            for coin in myacclongdevammi:
                if coin[0]==c:
                    if not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1 and is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        print(f"devam {c}")
                        return True  
                    elif not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1 and not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        close_position(c,"mylonglarACC")
                        print(f"{c} pozisyonu kapatıldı.")
                        return False
        for c in myshortlarACC:
            for coin in myaccshortdevammi:
                if coin[0]==c:
                    if not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1 and is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        print(f"devam {c}")
                        return True  
                    elif not is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1 and is_above_last_period_averageACC(coin[len(coin)-1], coin, 3)==49.1:
                        close_position(c,"mylonglarACC")
                        print(f"{c} pozisyonu kapatıldı.")
                        return False
    print(f"mylonglarACC: {mylonglarACC}")
    print(f"myacccoinlerlong: {myacccoinlerlong}")
    print(f"myacclongdevammi {myacclongdevammi}")
"""


def accdevammilistesiekle(coin,yon):
    if yon=="long":
        if coin in myacccoinlerlong:
            for c in myacclongdevammi:
                if c[0]==coin[0]:
                    c.append(coin[1])
                else:
                    myacclongdevammi.append(coin)
        else:
            myacccoinlerlong.append(coin)
            myacclongdevammi.append(coin)
    print(myacclongdevammi)
    if yon=="short":
        if coin in myacccoinlershort:
            for c in myaccshortdevammi:
                if c[0]==coin[0]:
                    c.append(coin[1])
                else:
                    myaccshortdevammi.append(coin)
        else:
            myacccoinlershort.append(coin)
            myaccshortdevammi.append(coin)
    print(myaccshortdevammi)

################################# Ana Fonksiyon

async def main():
    await telegram_client.start(phone=phone_number)
    @telegram_client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi:\n {event.raw_text}')

        if event.raw_text.startswith("Marketteki Tüm Coinlere Olan Nakit Girişi Raporu"): #IO
            AnaFonkIO(event.raw_text)

        if event.raw_text.startswith("???Canlı olan coin sayısı") and check_arrowsIO(mytextio[0]): #KA
            AnaFonkKA(event.raw_text)

        if event.raw_text.startswith("???Yapay zeka,") and check_arrowsIO(mytextio[0]): #Marketanaliz MA
            AnaFonkMA(event.raw_text)
        
        if event.raw_text.startswith("???Korelasyon Şiddeti Raporu (5m)"): #ci i d 5m
            AnaFonkCi(event.raw_text)

        if event.raw_text.startswith("???Sert Hareket Edenler"): #SDV
            AnaFonkSDV(event.raw_text)     

        if event.raw_text.startswith("???Marketteki Tüm Coinlere Olan en çok nakit girişi olanlar."): #IOF
            AnaFonkIOF(event.raw_text)   
        
        if event.raw_text.startswith("En Çok Panik Alım(Acc) Olan Coinler") or event.raw_text.startswith("En Çok Panik Satımı(Acc) Olan Coinler"): #IOF
            AnaFonkACC(event.raw_text) 

    while True:
        if 1: #io1d[len(io1d)-1]<altustsinir[0]:
            random.shuffle(mysent48)
            # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
           
            await telegram_client.send_message(target_user, mysent48[0]) #mysent[rastgele_komut()] )#'marketanaliz')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, "acc") #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent48[2]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, "acc") #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            #await asyncio.sleep(rastgele_sayi(100,200))
        
        if io1d[len(io1d)-1]>altustsinir[0] and io1d[len(io1d)-1]<altustsinir[1]:
            random.shuffle(mysent4849)
            await telegram_client.send_message(target_user, "io") #komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(20,50))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            if io1d[len(io1d)-1]>altustsinir[1] or io1d[len(io1d)-1]<altustsinir[0]:
                await telegram_client.send_message(target_user, "io") #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(50,100))
            else:
                await telegram_client.send_message(target_user, mysent4849[0]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
                await asyncio.sleep(rastgele_sayi(3000,5500))
        
        if io1d[len(io1d)-1]>altustsinir[1]:
            random.shuffle(mysent49)
            await telegram_client.send_message(target_user, komutlar[rastgele_sayi(0,len(komutlar)-1)])
            await asyncio.sleep(rastgele_sayi(35,100))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            await telegram_client.send_message(target_user, mysent49[0]) #mysent[rastgele_komut()] )#'marketanaliz')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[2]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[3]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[4]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(35,100))
            await telegram_client.send_message(target_user, mysent49[5]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
            await asyncio.sleep(rastgele_sayi(100,200))
        

with telegram_client:
    telegram_client.loop.run_until_complete(main())