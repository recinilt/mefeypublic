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
target_user = 'tradermikabot'  
alert_user = 'reccirik_bot'  
binance_api="PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
binance_secret="iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
binance_api_reccirik2="nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_reccirik2="WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"
binance_api_abim="W0cyfW6O27i7GsBKFYbm4zVjiOE0oY2lbOZYQwbYWksuDZG1zwt10x5w42GQ6JDa"
binance_secret_abim="FdrwJZG7zXTi3qwj9zQaxCb0YFWoYAZexGCTAP2QkUcMhV4dQuq5OGSQYgiQYioE"



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

    if convert_to_floatIO(text)<49: 
        print("!!!!!!!!!!!!!!!!!!!!! Piyasa Rikli !!!!!!!!!!!!!!!!!!!")
        return False
    else:
        print(">>>>>>>>>>>>>>>>>>>>>> Piyasa iyi durumda <<<<<<<<<<<<<<<<<<<<<<<<")
        return True


def convert_to_floatIOsure(text,sure):

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
        
#get_future_total_usdt_balance()

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
       

def yuvarla_0_5(sayi): # Sayıyı 0.5'in katlarına yuvarla 
    return round(sayi * 2) / 2



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




# Ana fonksiyondakiler: ############################################################################
def AnaFonkIO(raw_text):
    global symbolstrailingprices
    global calissinmi
    calissinmi=False
        
    
    mytextio.clear()
    mytextio.append(raw_text)
    io1d.append(convert_to_floatIO(mytextio[0]))
   
 
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


    print(f"Şuanki açık pozisyonların toplam kar zarar durumu: {round(sum(karzarardurumu),2)} USDT")

    trailing_dusen_coinler = fiyat_dalgalanma_takip(symbolstrailingprices, trailingyuzde)
    print(f" trailing düşen coinler: {trailing_dusen_coinler}")
    if trailing_dusen_coinler:
 
        for coin in trailing_dusen_coinler:
            close_position(coin,"mylonglarKA")
            mymesaj.append(coin)
            symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (coin,1.1),True)
            time.sleep(8)
    calissinmi=True
 
    if io1d[-1]-io1d[-2]>0.2 or io1d[-2]-io1d[-1]>0.19:
        print("BALİNAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("temiz KA toplayıcı trailing çalışıyor v3.py")

def AnaFonkKA(raw_text):
    global calissinmi
    calissinmi=False
    result = coin_veri_islemeKA(raw_text)
    #print(result)
    if io1d[-1]>48.9:
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
   
        
    else:
        print("io1d<altustsinir[1]")
    calissinmi=True

    
#

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
        
        

with telegram_client:
    telegram_client.loop.run_until_complete(main())