import re
from binance.client import Client



import time
from binance.enums import *

 

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
#exchange_info = binanceclient.futures_exchange_info()
#time.sleep(2)
#symbols = exchange_info['symbols']
#mysymbols3=[]
#for s in symbols:
#    mysymbols3.append(s['symbol'])
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
            threaded_close_position(pos["symbol"],"mylonglarGenel",kisi)
            print("Symbol kapatıldı", pos["symbol"])
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
        #if not symbol in mylonglarGenel:
        #    mylonglarGenel.append(symbol)
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
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")


#async########################
import threading

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
islemyapilacakkisi=input("işlem yapılacak kişi kim? (ben / abim / ikisi): ").lower()
alinacakmisatilacakmi=input(" buy / sell / close?: ").lower()
hepsimisatilacak="y"
islenecekcoin=""
kacxkaldirac=int(1)
harcanancost=float(0.1)
if alinacakmisatilacakmi=="close":
    hepsimisatilacak=input("hepsi mi satılacak (close)? (y/n): ")
if hepsimisatilacak=="n" or alinacakmisatilacakmi=="buy" or alinacakmisatilacakmi=="sell":
    islenecekcoin=input("işlem yapılacak coin çifti (örn. BTCUSDT): ").upper()
    kacxkaldirac=int(input("kaç x kaldıraç?: "))
    harcanancost=float(input("harcanan (kaldıraçla çarpılacak olan) cost kaç usdt? :"))

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

cozumleme()
############################## BİTTİ
