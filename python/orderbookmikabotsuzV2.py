import re
from binance.client import Client



import time
from binance.enums import *

import threading
import queue
import requests
import sys
 

print("program başlatılıyor...")


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
time.sleep(2)
symbols = exchange_info['symbols']
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s['symbol'])
print("Binancetaki futures coin çiftleri: \n",mysymbols3)
# Telegram Client'ı oluşturun
#patterler
pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
pattern2 = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')
patternSDV = r"✅✅(\w+)"
patternSDVtek = r"✅ (\w+)"
patternSDVasagicift = r"🔻🔻(\w+)"
patternSDVasagitek = r"🔻 (\w+)"
patternKA = r'\b(\w+)\s+TS:'
#Global değişkenler

mycost=3.5
myleverage=6
kactanbuyuk=17

mytextio=["merhaba"]
mylonglar=[]
myshortlar=[]
mylonglarGenel=[]
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

cirawtext=[]
acmakapamalistesi=[]
usdtlistem=[]
iopower=[]
yasaklilist=[]
symbolstrailingprices=[]
trailingyuzde=8 #yüzde düşünce kapanır.
trailingyuzde50altindayken=8

yuzdekackazanincakapatsin=2000
calissinmi=True
apkisa=[]
apuzun=[]
apalayimmi=True
apsatayimmi=False
apuzunalayimmi=True
apkisaalayimmi=True
ozelmesaj=[]
iokomutlari=[]
myshortlarGenel=[]



    
    


##################################### Yardımcı Fonksiyonlar:

def get_price(symbol):
    try:
        ticker = binanceclient.get_symbol_ticker(symbol=symbol.upper())
        time.sleep(2)
        return ticker['price']
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def myquantity(coin):
    return round(((get_my_cost_hazir*myleverage)/float(get_price(coin))),3)


def get_symbol_precision(symbol):
    try:
        info = binanceclient.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol.upper():
                return int(item['quantityPrecision'])
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        return None


def binle(coin):
    liste=["BONKUSDT","FLOKIUSDT","SATSUSDT","RATUSDT","PEPEUSDT","SHIBUSDT","CATUSDT","XUSDT","LUNCUSDT","XECUSDT"]
    for c in liste:
        if coin == c:
            return ("1000" + c)
        else:
            return coin


def eklesil(coin, liste, eylem):
    if eylem=="ekle":
        if liste=="mylonglarGenel" and not coin in mylonglarGenel:
            mylonglarGenel.append(coin)
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
        elif liste=="myshortlarGenel" and not coin in myshortlarGenel:
            myshortlarGenel.append(coin)
    if eylem=="sil":
        if liste=="mylonglarGenel" and coin in mylonglarGenel:
            mylonglarGenel.remove(coin)
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
        elif liste=="myshortlarGenel" and coin in myshortlarGenel:
            myshortlarGenel.remove(coin)

def get_future_total_usdt_balance():
    # Hesap bilgilerinizi alın
    futures_balance = binanceclient.futures_account_balance() 
    time.sleep(5)
    for balance in futures_balance: 
        if balance['asset'] == 'USDT':
            # İstediğiniz varlığı buraya girin 
            print(f"Available Balance: {balance['balance']}")
            return float(balance['balance'])
        else:
            return 100
    #time.sleep(5)
        
#get_future_total_usdt_balance()

def get_my_cost():
    mybalanceyuzde=(get_future_total_usdt_balance() * 0.03)
    my_cost=11/myleverage if mybalanceyuzde*myleverage<11 else mybalanceyuzde
    return my_cost

get_my_cost_hazir=get_my_cost()

############################ kar zarar durumu
# Açık pozisyonları al
def get_futures_positions():
    try:
        # Binance Futures account position endpoint
        account_info = binanceclient.futures_account()
        time.sleep(5)
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
        time.sleep(5)
        return result


    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []

def hepsinikapat(kisi):
    # Pozisyonları listele
    positions = get_futures_positions()
    print(positions)
    if positions:
        print("Açık Pozisyonlar:")
        for pos in positions:
            print(pos)
            threaded_close_position(pos["Symbol"],"mylonglarGenel",kisi)
            print("Symbol kapatıldı", pos["Symbol"])
    else:
        print("Açık pozisyon bulunamadı.")
#############################################

######################### CHATGPT DEĞİŞİKLİKLERİ BAŞLIYOR:
def buy_position(symbol, leverage, amount, liste, kisi="ben"):
    symbol=binle(symbol)
    try:
        
        # Binanceclient için işlem
        

        
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        time.sleep(2)
        if kisi=="ben" or kisi=="ikisi":
            #if binanceclient.futures_get_position_margin_type(symbol=symbol)['marginType']!="ISOLATED":
            try:
                binanceclient.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            except Exception as e:
                print(e)
            binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
            time.sleep(2)
            order1 = binanceclient.futures_create_order(
                symbol=symbol.upper(),
                side='BUY',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            time.sleep(2)
            print(order1)
        if kisi=="abim" or kisi=="ikisi":
            # Binanceclient_abim için işlem
            #binanceclient_abim.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            try:
                binanceclient_abim.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            except Exception as e:
                print(e)
            binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
            time.sleep(2)
            order2 = binanceclient_abim.futures_create_order(
                symbol=symbol.upper(),
                side='BUY',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            time.sleep(2)
            print(order2)

        #hesapla(symbol, "buy", 1)
        #eklesil(symbol, liste, "ekle")
        if not symbol in mylonglarGenel:
            mylonglarGenel.append(symbol)
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")

def sell_position(symbol, leverage, amount, liste, kisi):
    symbol=binle(symbol)
    try:
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        time.sleep(2)
        if kisi=="ben" or kisi=="ikisi":
            # Binanceclient için işlem
            #if binanceclient.futures_get_position_margin_type(symbol=symbol)['marginType']!="ISOLATED":
            try:
                binanceclient.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            except Exception as e:
                print(e)
            binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
            time.sleep(2)
            
            order1 = binanceclient.futures_create_order(
                symbol=symbol.upper(),
                side='SELL',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            time.sleep(2)
            print(order1)

        if kisi=="abim" or kisi=="ikisi":
            # Binanceclient_abim için işlem
            #binanceclient_abim.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            try:
                binanceclient_abim.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
            except Exception as e:
                print(e)
            binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
            time.sleep(2)
            order2 = binanceclient_abim.futures_create_order(
                symbol=symbol.upper(),
                side='SELL',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            time.sleep(2)
            print(order2)

        #hesapla(symbol, "sell", 1)
        #eklesil(symbol, liste, "ekle")
        if symbol not in myshortlarGenel:
            myshortlarGenel.append(symbol)
        time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

def close_position(coin, liste, kisi):
    coin=binle(coin)
    try:
        if kisi=="ben" or kisi=="ikisi":
            # Binanceclient için pozisyon kapatma
            positions = binanceclient.futures_position_information(symbol=coin)
            time.sleep(2)
            for position in positions:
                if float(position['positionAmt']) != 0:
                    side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
                    quantity = abs(float(position['positionAmt']))
                    #karzararesapla(coin, quantity, position['entryPrice'], get_price(coin), liste, 1 if side == "SIDE_BUY" else -1)

                    order1 = binanceclient.futures_create_order(
                        symbol=coin,
                        side=side,
                        type=ORDER_TYPE_MARKET,
                        quantity=quantity
                    )
                    time.sleep(2)
                    print(f"Pozisyon kapatıldı: {order1}")
                    if coin in mylonglarGenel:
                        mylonglarGenel.remove(coin)

        if kisi=="abim" or kisi=="ikisi":
            # Binanceclient_abim için pozisyon kapatma
            positions_abim = binanceclient_abim.futures_position_information(symbol=coin)
            time.sleep(2)
            for position in positions_abim:
                if float(position['positionAmt']) != 0:
                    side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
                    quantity = abs(float(position['positionAmt']))
                    #karzararesapla(coin, quantity, position['entryPrice'], get_price(coin), liste, 1 if side == "SIDE_BUY" else -1)

                    order2 = binanceclient_abim.futures_create_order(
                        symbol=coin,
                        side=side,
                        type=ORDER_TYPE_MARKET,
                        quantity=quantity
                    )
                    time.sleep(2)
                    print(f"Pozisyon kapatıldı: {order2}")
        eklesil(coin, liste, "sil")
        if coin in mylonglarGenel:
            mylonglarGenel.remove(coin)
        if coin in myshortlarGenel:
            mylonglarGenel.remove(coin)
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")


#async########################
#import threading

def threaded_buy_position(symbol, leverage, amount, liste, kisi):
    thread = threading.Thread(target=buy_position, args=(symbol, leverage, amount, liste,kisi))
    thread.start()

def threaded_sell_position(symbol, leverage, amount, liste,kisi):
    thread = threading.Thread(target=sell_position, args=(symbol, leverage, amount, liste,kisi))
    thread.start()

def threaded_close_position(symbol, liste,kisi):
    thread = threading.Thread(target=close_position, args=(symbol, liste,kisi))
    thread.start()

#coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
#for coin in coins:
#    threaded_buy_position(coin, 20, 1, "mylonglarGenel")


################
islemyapilacakkisi=""
while True:
    islemyapilacakkisi=input("işlem yapılacak kişi kim? (ben / abim / ikisi): ").lower()
    if islemyapilacakkisi=="ben" or islemyapilacakkisi=="abim" or islemyapilacakkisi=="ikisi":
        break
    else:
        print("geçerli bir seçenek giriniz")
#alinacakmisatilacakmi=input(" buy / sell / close?: ").lower()
hepsimisatilacak="y"
islenecekcoin=""
kacxkaldirac=int(1)
harcanancost=float(0.1)
#if alinacakmisatilacakmi=="close":
#    hepsimisatilacak=input("hepsi mi satılacak (close)? (y/n): ")
#if hepsimisatilacak=="n" or alinacakmisatilacakmi=="buy" or alinacakmisatilacakmi=="sell":
#    islenecekcoin=input("işlem yapılacak coin çifti (örn. BTCUSDT): ").upper()
#    kacxkaldirac=int(input("kaç x kaldıraç?: "))
#    harcanancost=float(input("harcanan (kaldıraçla çarpılacak olan) cost kaç usdt? :"))

def cozumleme():
    if alinacakmisatilacakmi.lower()=="buy":
        threaded_buy_position(islenecekcoin,kacxkaldirac,harcanancost,"mylonglarGenel",islemyapilacakkisi)
    elif alinacakmisatilacakmi.lower()=="sell":
        threaded_sell_position(islenecekcoin,kacxkaldirac,harcanancost,"myshortlarGenel",islemyapilacakkisi)
    elif alinacakmisatilacakmi.lower()=="close":
        if hepsimisatilacak.lower()=="n":
            threaded_close_position(islenecekcoin,"mylonglarGenel",islemyapilacakkisi)
        if hepsimisatilacak.lower()=="y":
            hepsinikapat(islemyapilacakkisi)
    else:
        print("lütfen parantez içlerindeki cevaplardan birini veriniz.")
    print("işlem yapılıyor...")
    time.sleep(5)

#cozumleme()
############################## BİTTİ

#import requests

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
    satis = order_book['asks']  # Satış emirleri (fiyat, miktar)
    alis = order_book['bids']  # Alış emirleri (fiyat, miktar)

    # Mevcut fiyatı belirle (En düşük satış emri)
    current_price = float(satis[0][0])

    # Hedef fiyat aralıklarını hesapla
    upper_limit = current_price * (1 + percentage_threshold / 100)
    lower_limit = current_price * (1 - percentage_threshold / 100)

    # Belirlenen yüzdelik aralıklara göre emir miktarlarını topla
    satis_sum = sum(float(amount) for price, amount in satis if float(price) <= upper_limit)
    alis_sum = sum(float(amount) for price, amount in alis if float(price) >= lower_limit)

    return [alis_sum, satis_sum, round((alis_sum/satis_sum),2)]

# Örnek kullanım: 'BTCUSDT' için emir toplamları
result = calculate_order_sum('BTCUSDT')
print(result)

coins=['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'ENJUSDT', 'FLMUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LITUSDT', 'UNFIUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'BTCSTUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT', '1000SHIBUSDT', 'BAKEUSDT', 'GTCUSDT', 'BTCDOMUSDT', 'IOTXUSDT', 'RAYUSDT', 'C98USDT', 'MASKUSDT', 'ATAUSDT', 'DYDXUSDT', '1000XECUSDT', 'GALAUSDT', 'CELOUSDT', 'ARUSDT', 'KLAYUSDT', 'ARPAUSDT', 'CTSIUSDT', 'LPTUSDT', 'ENSUSDT', 'PEOPLEUSDT', 'ROSEUSDT', 'DUSKUSDT', 'FLOWUSDT', 'IMXUSDT', 'API3USDT', 'GMTUSDT', 'APEUSDT', 'WOOUSDT', 'FTTUSDT', 'JASMYUSDT', 'DARUSDT', 'OPUSDT', 'INJUSDT', 'STGUSDT', 'SPELLUSDT', '1000LUNCUSDT', 'LUNA2USDT', 'LDOUSDT', 'CVXUSDT', 'ICPUSDT', 'APTUSDT', 'QNTUSDT', 'FETUSDT', 'FXSUSDT', 'HOOKUSDT', 'MAGICUSDT', 'TUSDT', 'HIGHUSDT', 'MINAUSDT', 'ASTRUSDT', 'AGIXUSDT', 'PHBUSDT', 'GMXUSDT', 'CFXUSDT', 'STXUSDT', 'BNXUSDT', 'ACHUSDT', 'SSVUSDT', 'CKBUSDT', 'PERPUSDT', 'TRUUSDT', 'LQTYUSDT', 'USDCUSDT', 'IDUSDT', 'ARBUSDT', 'JOEUSDT', 'TLMUSDT', 'AMBUSDT', 'LEVERUSDT', 'RDNTUSDT', 'HFTUSDT', 'XVSUSDT', 'ETHBTC', 'BLURUSDT', 'EDUUSDT', 'IDEXUSDT', 'SUIUSDT', '1000PEPEUSDT', '1000FLOKIUSDT', 'UMAUSDT', 'RADUSDT', 'KEYUSDT', 'COMBOUSDT', 'NMRUSDT', 'MAVUSDT', 'MDTUSDT', 'XVGUSDT', 'WLDUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'AGLDUSDT', 'YGGUSDT', 'DODOXUSDT', 'BNTUSDT', 'OXTUSDT', 'SEIUSDT', 'CYBERUSDT', 'HIFIUSDT', 'ARKUSDT', 'GLMRUSDT', 'BICOUSDT', 'STRAXUSDT', 'LOOMUSDT', 'BIGTIMEUSDT', 'BONDUSDT', 'ORBSUSDT', 'STPTUSDT', 'WAXPUSDT', 'BSVUSDT', 'RIFUSDT', 'POLYXUSDT', 'GASUSDT', 'POWRUSDT', 'SLPUSDT', 'TIAUSDT', 'SNTUSDT', 'CAKEUSDT', 'MEMEUSDT', 'TWTUSDT', 'TOKENUSDT', 'ORDIUSDT', 'STEEMUSDT', 'BADGERUSDT', 'ILVUSDT', 'NTRNUSDT', 'KASUSDT', 'BEAMXUSDT', '1000BONKUSDT', 'PYTHUSDT', 
'SUPERUSDT', 'USTCUSDT', 'ONGUSDT', 'ETHWUSDT', 'JTOUSDT', '1000SATSUSDT', 'AUCTIONUSDT', '1000RATSUSDT', 'ACEUSDT', 'MOVRUSDT', 'NFPUSDT', 'BTCUSDC', 'ETHUSDC', 'BNBUSDC', 'SOLUSDC', 'XRPUSDC', 'AIUSDT', 'XAIUSDT', 'DOGEUSDC', 'WIFUSDT', 'MANTAUSDT', 'ONDOUSDT', 'LSKUSDT', 'ALTUSDT', 'JUPUSDT', 'ZETAUSDT', 'RONINUSDT', 'DYMUSDT', 'SUIUSDC', 'OMUSDT', 'LINKUSDC', 'PIXELUSDT', 'STRKUSDT', 'MAVIAUSDT', 'ORDIUSDC', 'GLMUSDT', 'PORTALUSDT', 'TONUSDT', 'AXLUSDT', 'MYROUSDT', '1000PEPEUSDC', 'METISUSDT', 'AEVOUSDT', 'WLDUSDC', 'VANRYUSDT', 'BOMEUSDT', 'ETHFIUSDT', 'AVAXUSDC', '1000SHIBUSDC', 'ENAUSDT', 'WUSDT', 'WIFUSDC', 'BCHUSDC', 'TNSRUSDT', 'SAGAUSDT', 'LTCUSDC', 'NEARUSDC', 'TAOUSDT', 'OMNIUSDT', 'ARBUSDC', 'NEOUSDC', 'FILUSDC', 'TIAUSDC', 'BOMEUSDC', 'REZUSDT', 'ENAUSDC', 'ETHFIUSDC', '1000BONKUSDC', 'BBUSDT', 'NOTUSDT', 'TURBOUSDT', 'IOUSDT', 'ZKUSDT', 'MEWUSDT', 'LISTAUSDT', 'ZROUSDT', 'BTCUSDT_241227', 'ETHUSDT_241227', 'CRVUSDC', 'RENDERUSDT', 'BANANAUSDT', 'RAREUSDT', 'GUSDT', 'SYNUSDT', 'SYSUSDT', 'VOXELUSDT', 'BRETTUSDT', 'ALPACAUSDT', 'POPCATUSDT', 'SUNUSDT', 'VIDTUSDT', 'NULSUSDT', 'DOGSUSDT', 'MBOXUSDT', 'CHESSUSDT', 'FLUXUSDT', 'BSWUSDT', 'QUICKUSDT', 'NEIROETHUSDT', 'RPLUSDT', 'AERGOUSDT', 'POLUSDT', 'UXLINKUSDT', '1MBABYDOGEUSDT', 'NEIROUSDT', 'KDAUSDT', 'FIDAUSDT', 'FIOUSDT', 'CATIUSDT', 'GHSTUSDT', 'LOKAUSDT', 'HMSTRUSDT', 'BTCUSDT_250328', 'ETHUSDT_250328', 'REIUSDT', 'COSUSDT', 'EIGENUSDT', 'DIAUSDT', '1000CATUSDT', 'SCRUSDT', 'GOATUSDT', 'MOODENGUSDT', 'SAFEUSDT', 'SANTOSUSDT', 'TROYUSDT', 'PONKEUSDT', 'COWUSDT', 'CETUSUSDT', '1000000MOGUSDT', 'GRASSUSDT', 'DRIFTUSDT', 'SWELLUSDT', 'ACTUSDT', 'PNUTUSDT', 'HIPPOUSDT', '1000XUSDT', 'DEGENUSDT', 'BANUSDT', 'AKTUSDT', 'SLERFUSDT', 'SCRTUSDT', '1000CHEEMSUSDT', '1000WHYUSDT', 'THEUSDT', 'MORPHOUSDT', 'CHILLGUYUSDT', 'KAIAUSDT', 'AEROUSDT', 'ACXUSDT', 'ORCAUSDT', 'MOVEUSDT', 'RAYSOLUSDT', 'KOMAUSDT', 'VIRTUALUSDT', 'SPXUSDT', 'MEUSDT', 'AVAUSDT', 'DEGOUSDT', 'VELODROMEUSDT', 'MOCAUSDT', 'VANAUSDT']
#symbols = ['btcusdt', 'ethusdt', 'bnbusdt']
symbols=coins[:100]
total=[]
def longlarıtara(oran):
    longacilacaklar=[]
    for mycoin in symbols:
        print("değerlendirilen coin: ",mycoin)
        result=1
        try:
            result = calculate_order_sum(mycoin)[2]
        except Exception as e:
            print("hata: ", e)
        total.append(result)
        if result>oran:
            longacilacaklar.append([mycoin,result])
            print("LONG>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>: ", mycoin, result)
    if longacilacaklar:
        longacilacaklar.sort(key=lambda x: x[1], reverse=True)
    return longacilacaklar

#print(longlarıtara())

#########
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

tumoranlist=[]

def cift_ema_sinyal(liste=tumoranlist, kisa_span=5, uzun_span=20):
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
    return [kisa_ema >= uzun_ema, kisa_ema < uzun_ema]  # Kısa EMA uzun EMA'dan büyükse AL (True), aksi halde SAT (False)
    #return [io1d[-1]>uzun_ema, io1d[-1]<uzun_ema]

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

def fiyat_dalgalanma_takip_ob(ssrtrailinglist, mysymbol):
    for coin in ssrtrailinglist:
        symbol, ssrlist = coin
        if symbol == mysymbol:
            return cift_ema_sinyal(ssrlist)[0]
    return True  # Eğer aranan sembol bulunamazsa None döndür

#####################
    

#############################thread
import threading
import time
import queue
class StoppableThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self._stop_event = threading.Event()
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            while not self._stop_event.is_set():
                self._target(*self._args, **self._kwargs)
                time.sleep(0.1)
        except Exception as e:
            print(f"Thread hata verdi: {e}")

    def stop(self):
        self._stop_event.set()

# Kullanıcı input'unu timeout ile almak
def timed_input(prompt, timeout):
    q = queue.Queue()

    def input_thread():
        try:
            q.put(input(prompt))
        except EOFError:
            q.put(None)

    thread = threading.Thread(target=input_thread, daemon=True)  # Daemon thread
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("Süre doldu, cevap verilmedi.")
        return None
    else:
        return q.get()

# Thread içinde çalışacak fonksiyon
def ask_name():
    global tumorankactanbuyukoluncaalsin
    result = timed_input("tumorankactanbuyukoluncaalsin ", 5)
    if result:
        print(f"Girilen sayı: {result}")
        tumorankactanbuyukoluncaalsin=result
    else:
        print("Zaman aşımı! İsim girilmedi.")

# Thread başlatma ve durdurma fonksiyonları
def start_thread(target_function):
    t = StoppableThread(target=target_function)
    t.daemon = True  # Daemon thread olarak işaretle
    t.start()
    return t

def stop_thread(thread):
    thread.stop()
    thread.join(1)  # Thread kapanması için max 1 saniye bekle
    print("Thread durduruldu.")

"""
# Kullanım örneği: While Döngüsü
if __name__ == "__main__":
    try:
        while True:  # Döngü başlat
            print("\nYeni döngü başlıyor...")
            
            # Kullanıcıdan input almak için thread başlat
            thread = start_thread(ask_name)
            
            # 5 saniye bekle
            time.sleep(5)
            
            # Thread'i durdur
            stop_thread(thread)
            
            # Diğer işlemler
            print("Diğer işlemler devam ediyor...\n")
            
            # Döngüyü sonlandırmak için bir kontrol ekleyelim
            if input("Çıkmak için 'q' tuşuna basın, devam etmek için Enter'a basın: ").strip().lower() == 'q':
                print("Program sonlandırılıyor...")
                break
            print("yeni döngü: ")
            tarananlar=longlarıtara(2)
            taranansemboller= [item[0] for item in tarananlar]
            #total = sum(item[1] for item in tarananlar)
            mytotal=sum(total)
            tumoran=mytotal/len(total)
            tumoranlist.append(tumoran)
            print("tümoran: ",tumoran)
            if tumoran>1.3 and cift_ema_sinyal()[1]:
                if mylonglarGenel:
                    for coin in mylonglarGenel:
                        if not coin in taranansemboller:
                            threaded_close_position(coin,"mylonglarGenel",islemyapilacakkisi)
            if (tumoran<tumorankactankucukoluncasatsin and cift_ema_sinyal()[1]) or tumoran<tumorankactankucukoluncasatsin:
                print("tümoran ", tumorankactankucukoluncasatsin," altında. hepsi kapanıyor...")
                if mylonglarGenel:
                    hepsinikapat(islemyapilacakkisi)
            if tumoran>tumorankactanbuyukoluncaalsin and cift_ema_sinyal()[0]:
                for coinac in taranansemboller:
                    if not coinac in mylonglarGenel:
                        threaded_buy_position(coinac,6,1.8,"mylonglarGenel",islemyapilacakkisi)
            total.clear()
            time.sleep(40)

    except KeyboardInterrupt:
        print("Program durduruldu.")

"""
#from playsound import playsound
import winsound

# WAV dosyasının yolu
hepsinikapatsesi = "asagi.wav"
alsesi="alsesi.wav"
satsesi="satsesi.wav"

# Seslendirme
#playsound(dosya_yolu)

#############################thread bitiş


####################btcEMA
import pandas as pd
import numpy as np
#from binance.client import Client

def analyze_market():
    # Binance API Client'ı başlatın
    global binanceclient
    #client = Client(api_key, api_secret)

    try:
        # BTC/USDT paritesi için son 300 kapanış fiyatını alın
        klines = binanceclient.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=300)
        
        # Kapanış fiyatlarını bir listeye dönüştürün
        close_prices = [float(kline[4]) for kline in klines]
        
        # Son fiyatı alın
        current_price = close_prices[-1]

        # Yüzde 3 aşağı ve yukarı fiyatları hesaplayın
        lower_bound = current_price * 0.97
        upper_bound = current_price * 1.03

        # Emir defteri verilerini alın
        order_book = binanceclient.get_order_book(symbol="BTCUSDT")
        
        # Alış ve satış emirlerini işleyin
        buy_orders = [float(order[1]) for order in order_book['bids'] if float(order[0]) >= lower_bound]
        sell_orders = [float(order[1]) for order in order_book['asks'] if float(order[0]) <= upper_bound]

        total_buy_orders = sum(buy_orders)
        total_sell_orders = sum(sell_orders)

        # EMA'ları hesaplayın
        short_ema = pd.Series(close_prices).ewm(span=27).mean().iloc[-1]
        long_ema = pd.Series(close_prices).ewm(span=147).mean().iloc[-1]

        # Koşulları kontrol edin
        if short_ema > long_ema: #and total_buy_orders / total_sell_orders > 1:
            return True
        else:
            return False

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False

# Kullanım örneği
#result = analyze_market()
#print(result)

##########################btcEMA bitiş
tumorankactanbuyukoluncaalsin=1.1
tumorankactankucukoluncasatsin=1.05

giris = [1.4]
while True:
    
    print("yeni döngü: ")
    #######soru
    """
    print("Thread başlatıldı. 5 saniye içinde sayı girin...")
    thread = start_thread(ask_name)
    
    # 5 saniye bekle
    time.sleep(6)  # Ekstra güvenlik için 6 saniye
    stop_thread(thread)

    

    #print("Giriş:", tumorankactanbuyukoluncaalsin)
    """
    ###########
    if True:
        tarananlar=longlarıtara(1.7)
        btcdurumu = analyze_market()
        taranansemboller= [item[0] for item in tarananlar]
        #total = sum(item[1] for item in tarananlar)
        mytotal=sum(total)
        tumoran=mytotal/len(total)
        tumoranlist.append(tumoran)
        print("tümoran: ",tumoran)
        if tumoran>1.1 and cift_ema_sinyal()[1]:
            if mylonglarGenel:
                for coin in mylonglarGenel:
                    if not coin in taranansemboller:
                        threaded_close_position(coin,"mylonglarGenel",islemyapilacakkisi)
                        winsound.PlaySound(satsesi, winsound.SND_FILENAME)
                        
        if (tumoran<tumorankactankucukoluncasatsin and cift_ema_sinyal()[1]) or tumoran<tumorankactankucukoluncasatsin or btcdurumu==False:
            print("Tüm Oran: ", tumoran, ". BTC yükselişte mi? ", btcdurumu, ". Hepsi kapanıyor...")
            #print("tümoran ", tumorankactankucukoluncasatsin," altında. veya da kısa ema uzun emanın altında. hepsi kapanıyor...")
            if mylonglarGenel:
                hepsinikapat(islemyapilacakkisi)
                winsound.PlaySound(hepsinikapatsesi, winsound.SND_FILENAME)
                
        if tumoran>tumorankactanbuyukoluncaalsin and btcdurumu:
            for coinac in taranansemboller:
                if not coinac in mylonglarGenel:
                    threaded_buy_position(coinac,6,1.8,"mylonglarGenel",islemyapilacakkisi)
                    winsound.PlaySound(alsesi, winsound.SND_FILENAME)
                
        total.clear()
        time.sleep(40)
    time.sleep(10)

    

