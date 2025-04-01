from telethon import TelegramClient, events
from binance.client import Client
import asyncio
import re
import random
import time
from binance.enums import *

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
mysent=["sdv","marketanaliz","io","ci i d 5m","ka","iof"]
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

def close_position(coin):
    # Mevcut pozisyonu kapat
    positions = binanceclient.futures_position_information(symbol=coin)
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            order = binanceclient.futures_create_order(
                symbol=coin,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=abs(float(position['positionAmt']))
            )
            print(f"Pozisyon kapatıldı: {order}")
            time.sleep(5)  # 5 saniye bekle

def get_symbol_precision(symbol):
    try:
        info = binanceclient.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol.upper():
                return int(item['quantityPrecision'])
    except Exception as e:
        print(f"Error: {e}")
        return None

def open_position(symbol, leverage, amount):
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
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")

def sell_position(symbol, leverage, amount):
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
        return None

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


# Ana fonksiyondakiler:
def AnaFonkIO(raw_text):
    mytextio.clear()
    mytextio.append(raw_text)
    if not check_arrowsIO(mytextio[0]): #re.search(pattern_15m, event.raw_text) and re.search(pattern_1h, event.raw_text) and re.search(pattern_4h, event.raw_text):
        print("Piyasa riskli!!!!!!!!!!!!!!!!!")
        if len(mylonglarKA)>0:
            for coin in mylonglarKA:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarKA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        if len(mylonglarMA)>0:
            for coin in mylonglarMA:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarMA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        if len(mylonglarSDV)>0:    
            for coin in mylonglarSDV:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarSDV.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        if len(mylonglarIOF)>0:    
            for coin in mylonglarIOF:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarIOF.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        if len(mylonglarCi)>0:    
            for coin in mylonglarCi:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarCi.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
    else:
        print("piyasa iyi durumda.>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")
    print(f"Longlar:\nCi:{mylonglarCi}\nIOF:{mylonglarIOF}\nSDV:{mylonglarSDV}\nKA:{mylonglarKA}\nMA:{mylonglarMA}")
    print(f"Shortlar:\nCi:{myshortlarCi}\nIOF:{myshortlarIOF}\nSDV:{myshortlarSDV}")            
def AnaFonkKA(raw_text):
    #[1,???], ['ETHUSDT', 1.2, 1.1, 1.048, 788, True, 7.3]
    #TRX TS:1,6 MTS:1,4 PT:1,048 Dk:288✅ Kar:%7,6 😍 Grafik (http://tradingview.com/chart/?symbol=BINANCE:TRXUSDT)

    result = extract_coin_dataKA(raw_text)
    if result[0][0]>1:
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
                mylonglarKA.append(coin)
                open_position(coin, myleverage, mycost)
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        
        for coin in mylonglarKA:
            if coin in kadakilonglar:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarKA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print(f"Longlar:{mylonglarKA}")

def AnaFonkMA(raw_text):
    #matchesMA = re.findall(patternMA2, event.raw_text)
    #resultMA = [[match[0], float(match[1].replace(',', '.')), float(match[2].replace(',', '.')), float(match[3]), float(match[4].replace(',', '.'))] for match in matchesMA]
    
    if "Btc düşüş trendinde olduğu için," in raw_text:
        for coin in mylonglarMA:
            close_position(coin)
            print(f"{coin} pozisyonu kapatıldı.")
            mylonglarMA.remove(coin)
            #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print("Btc düşüş trendinde olduğu için, çalışmadı.")

    else:
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
                mylonglarMA.append(coin)
                open_position(coin, myleverage, mycost)
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in mylonglarMA:
            if coin in longacMA:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarMA.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        print(f"Longlar:{mylonglarMA}")

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
    if check_arrowsIO(mytextio[0]): #len(combined_list) > 0: 
        mySDVlist=[]
        for coin in combined_list:
            if binle(coin) in mysymbols3 and acabilirmiyim(binle(coin)):
                mySDVlist.append(binle(coin))

        for coin in mySDVlist:
            if coin in mylonglarSDV:
                print(f"{coin} zaten vardı")
            else:
                mylonglarSDV.append(coin)
                open_position(coin, myleverage, mycost)
                print(f"{coin} long açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in mylonglarSDV:
            if coin in mySDVlist:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarSDV.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        mylonglar=mylonglarSDV

    if not check_arrowsIO(mytextio[0]): #len(combined_list2) > 0: 
        mySDVlist=[]
        for coin in combined_list2:
            if binle(coin) in mysymbols3 and acabilirmiyim(binle(coin)):
                mySDVlist.append(binle(coin))

        for coin in mySDVlist:
            if coin in myshortlarSDV:
                print(f"{coin} zaten vardı")
            else:
                myshortlarSDV.append(coin)
                sell_position(coin, myleverage, mycost)
                print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in myshortlarSDV:
            if coin in mySDVlist:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                myshortlarSDV.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        myshortlar=myshortlarSDV
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
    
    if check_arrowsIO(mytextio[0]):
        for coin in longAc:
            if coin in mylonglarCi:
                print(f"{coin} zaten vardı")
            else:
                mylonglarCi.append(coin)
                open_position(coin, myleverage, mycost)
                print(f"{coin} long açıldı")
                #await telegram_client.send_message(alert_user, f"{coin}'a LONG posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        for coin in mylonglarCi:
            if coin in longAc:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarCi.remove(coin)
            #await telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")     
        if len(myshortlarCi)>0:
            for coin in myshortlarCi:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                myshortlarCi.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")   
    
    if not check_arrowsIO(mytextio[0]):
        for coin in shortAc:
            if coin in myshortlarCi:
                print(f"{coin} zaten vardı")
            else:
                myshortlarCi.append(coin)
                sell_position(coin, myleverage, mycost)
                print(f"{coin} short açıldı")
                #await telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")
        for coin in myshortlarCi:
            if coin in shortAc:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                myshortlarCi.remove(coin)
                #await telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
        if len(mylonglarCi)>0:
            for coin in mylonglarCi:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarCi.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")   
    print(f"Shortlar:{myshortlarCi}")
    print(f"Longlar:{mylonglarCi}")
    
def AnaFonkIOF(raw_text):
    #OXTUSDT 7,0X Payı:%3,7 Pahalılık:8,0 🔼🔻🔻🔼🔼 Grafik (http://tradingview.com/chart/?symbol=BINANCE:OXTUSDT)
    #['TIAUSDT', 0.4, 0.9, 1.9, [True, True, True, False, True]]
    
    parsed_data = parse_usdt_dataIOF(raw_text)
    if check_arrowsIO(mytextio[0]):
        longAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]>1 and entry[2]>0.5 and entry[3]<5 and entry[4][0] and entry[4][1] and entry[4][2] and entry[4][3]:
                longAc.append(binle(entry[0]))

        for coin in longAc:
            if coin in mylonglarIOF:
                print(f"{coin} zaten vardı")
            else:
                if check_arrowsIO(mytextio[0]):
                    mylonglarIOF.append(coin)
                    open_position(coin, myleverage, mycost)
                    print(f"{coin} long açıldı")
        
        for coin in mylonglarIOF:
            if coin in longAc:
                print(f"{coin} 'e zaten long açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                mylonglarIOF.remove(coin)
        
    if not check_arrowsIO(mytextio[0]): #len(combined_list2) > 0: 
        shortAc=[]
        for entry in parsed_data:
            if binle(entry[0]) in mysymbols3 and acabilirmiyim(binle(entry[0])) and entry[1]<1.7 and entry[2]>0.5 and entry[3]>0.5 and not entry[4][0] and not entry[4][1] and not entry[4][2] and not entry[4][3] and not entry[4][4]:
                shortAc.append(binle(entry[0]))

        for coin in shortAc:
            if coin in myshortlarIOF:
                print(f"{coin} zaten vardı")
            else:
                myshortlarIOF.append(coin)
                sell_position(coin, myleverage, mycost)
                print(f"{coin} short açıldı")
                #telegram_client.send_message(alert_user, f"{coin}'a SHORT posizyon açıldı. büyüklüğü: {myleverage}x kaldıraçlı, {mycost} USDT harcamalı, yani {myleverage * mycost} dolar büyüklüğünde.")

        for coin in myshortlarIOF:
            if coin in shortAc:
                print(f"{coin} 'e zaten short açılmış.")
            else:
                close_position(coin)
                print(f"{coin} pozisyonu kapatıldı.")
                myshortlarIOF.remove(coin)
                #telegram_client.send_message(alert_user, f"{coin}'in future pozisyonu KAPATILDI.")
    print(f"Longlar:{mylonglarIOF}")
    print(f"Shortlar:{myshortlarIOF}")
    

    
################################# Ana Fonksiyon

async def main():
    await telegram_client.start(phone=phone_number)

    @telegram_client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi: {event.raw_text}')

        if event.raw_text.startswith("Marketteki Tüm Coinlere Olan Nakit Girişi Raporu"): #IO
            AnaFonkIO(event.raw_text)

        if event.raw_text.startswith("Canlı olan coin sayısı") and check_arrowsIO(mytextio[0]): #KA
            AnaFonkKA(event.raw_text)

        if event.raw_text.startswith("Yapay zeka,") and check_arrowsIO(mytextio[0]): #Marketanaliz MA
            AnaFonkMA(event.raw_text)
        
        if event.raw_text.startswith("Korelasyon Şiddeti Raporu (5m)"): #ci i d 5m
            AnaFonkCi(event.raw_text)

        if event.raw_text.startswith("Sert Hareket Edenler"): #SDV
            AnaFonkSDV(event.raw_text)     

        if event.raw_text.startswith("Marketteki Tüm Coinlere Olan en çok nakit girişi olanlar."): #IOF
            AnaFonkIOF(event.raw_text)    
    while True:
        #rastgele_kelimeler(kelime_listesi_sdv_ma)
        #rastgele_komut()
        random.shuffle(mysent)
        await telegram_client.send_message(target_user, komutlar[rastgele_sayi(0,len(komutlar)-1)])
        await asyncio.sleep(rastgele_sayi(20,50))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
        await telegram_client.send_message(target_user, mysent[0]) #mysent[rastgele_komut()] )#'marketanaliz')
        await asyncio.sleep(rastgele_sayi(20,50))
        await telegram_client.send_message(target_user, mysent[1]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
        await asyncio.sleep(rastgele_sayi(20,50))
        await telegram_client.send_message(target_user, mysent[2]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
        await asyncio.sleep(rastgele_sayi(20,50))
        await telegram_client.send_message(target_user, mysent[3]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
        await asyncio.sleep(rastgele_sayi(20,50))
        await telegram_client.send_message(target_user, mysent[4]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
        await asyncio.sleep(rastgele_sayi(20,50))
        await telegram_client.send_message(target_user, mysent[5]) #mysent[1] if kacinci == 0 else mysent[0])#'sdv')
        await asyncio.sleep(rastgele_sayi(100,200))
        

with telegram_client:
    telegram_client.loop.run_until_complete(main())