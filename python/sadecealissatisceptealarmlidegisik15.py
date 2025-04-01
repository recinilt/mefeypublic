#from telethon import TelegramClient, events
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
import os
#import pandas as pd


def print_filename():
    # Mevcut dosyanın tam yolunu alır
    file_path = __file__
    # Sadece dosya adını almak için
    file_name = os.path.basename(file_path)
    # Dosya adını konsola yazdır
    print(file_name)

# Fonksiyonu çağırarak dosya adını yazdır
print_filename()


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
time.sleep(2)
symbols = exchange_info['symbols']
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s['symbol']),
# Telegram Client'ı oluşturun
#telegram_client = TelegramClient('session_name', telegram_api_id, telegram_api_hash)
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
ilkio=50#float(input("io rakamını giriniz:"))
ilkkackez=20#int(input("kaç tane io eklensin?"))
for i in range(1, ilkkackez + 1):
    #print(i)
    io1d.append(ilkio)
cirawtext=[]
acmakapamalistesi=[]
usdtlistem=[]
iopower=[]
yasaklilist=["ETHUSDT","SOLUSDT","BTCUSDT","USDCUSDT"]
symbolstrailingprices=[]
trailingyuzde=8 #yüzde düşünce kapanır.
trailingyuzde50altindayken=4

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
    
def rastgele_sayi(min_deger, max_deger):
    return random.randint(min_deger, max_deger)

def get_price(symbol):
    try:
        ticker = binanceclient.get_symbol_ticker(symbol=symbol.upper())
        time.sleep(1)
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
        time.sleep(1)
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
    time.sleep(1)
    for balance in futures_balance: 
        if balance['asset'] == 'USDT':
            # İstediğiniz varlığı buraya girin 
            print(f"Available Balance: {balance['balance']}")
            return float(balance['balance'])
        else:
            return 100
    #time.sleep(5)
        
get_future_total_usdt_balance()

def get_my_cost():
    mybalanceyuzde=(get_future_total_usdt_balance() * 0.018)
    my_cost=11/myleverage if mybalanceyuzde*myleverage<10.5 else mybalanceyuzde
    return mycost

get_my_cost_hazir=get_my_cost()


def get_futures_positions():
    try:
        # Binance Futures account position endpoint
        account_info = binanceclient.futures_account()
        time.sleep(1)
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
        time.sleep(1)
        return result


    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []


######################### CHATGPT DEĞİŞİKLİKLERİ BAŞLIYOR:
def buy_position(symbol, leverage, amount, liste):
    symbol=binle(symbol)
    try:
        # Binanceclient için işlem
        binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
        #time.sleep(2)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        #time.sleep(2)
        
        order1 = binanceclient.futures_create_order(
            symbol=symbol.upper(),
            side='BUY',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        #time.sleep(2)
        print(order1)

        if False:
            # Binanceclient_abim için işlem
            binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
            #time.sleep(2)
            order2 = binanceclient_abim.futures_create_order(
                symbol=symbol.upper(),
                side='BUY',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            #time.sleep(2)
            print(order2)

        #hesapla(symbol, "buy", 1)
        eklesil(symbol, liste, "ekle")
        if not symbol in mylonglarGenel:
            mylonglarGenel.append(symbol)
        #time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")

def sell_position(symbol, leverage, amount, liste):
    symbol=binle(symbol)
    try:
        # Binanceclient için işlem
        binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
        #time.sleep(1)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclient.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        #time.sleep(1)
        order1 = binanceclient.futures_create_order(
            symbol=symbol.upper(),
            side='SELL',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        #time.sleep(1)
        print(order1)

        if False:
            # Binanceclient_abim için işlem
            binanceclient_abim.futures_change_leverage(symbol=symbol, leverage=leverage)
            #time.sleep(1)
            order2 = binanceclient_abim.futures_create_order(
                symbol=symbol.upper(),
                side='SELL',
                type='MARKET',
                quantity=quantity,
                leverage=leverage
            )
            #time.sleep(1)
            print(order2)

        #hesapla(symbol, "sell", 1)
        eklesil(symbol, liste, "ekle")
        #time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

def close_position(coin, liste):
    coin=binle(coin)
    try:
        # Binanceclient için pozisyon kapatma
        positions = binanceclient.futures_position_information(symbol=coin)
        #time.sleep(2)
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
                #time.sleep(2)
                print(f"Pozisyon kapatıldı: {order1}")
                if coin in mylonglarGenel:
                    mylonglarGenel.remove(coin)
        if False:
            # Binanceclient_abim için pozisyon kapatma
            positions_abim = binanceclient_abim.futures_position_information(symbol=coin)
            #time.sleep(2)
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
                    #time.sleep(2)
                    print(f"Pozisyon kapatıldı: {order2}")
        eklesil(coin, liste, "sil")
        #time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
############################## BİTTİ

def BTCdurumu():
    yukselisdusus=[]
    try:
        klines = binanceclient.futures_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=4)
        open_prices = [float(kline[1]) for kline in klines]
        close_prices = [float(kline[4]) for kline in klines]
        if close_prices[-1]>open_prices[-1] and open_prices[-1]>open_prices[-2] and open_prices[-2]>open_prices[-3] : #and open_prices[-3]>open_prices[-4]:
            yukselisdusus.append(True)
        else:
            yukselisdusus.append(False)
        
        if close_prices[-1]<open_prices[-1] and open_prices[-1]<open_prices[-2] and open_prices[-2]<open_prices[-3] :#and open_prices[-3]<open_prices[-4]:
            yukselisdusus.append(True)
        else:
            yukselisdusus.append(False)
        return yukselisdusus
    except Exception as e:
        print(f"Error with symbol BTCUSDT: {str(e)}")

def dusenler_satis():
    #exchange_info = binanceclient.futures_coin_exchange_info()
    # Sembol formatını kontrol etmek için
    #symbols = [s['symbol'] for s in exchange_info['symbols'] if 'USD' in s['quoteAsset']]
    #print("Kullanılabilir Semboller:", symbols)

    top_100_symbols = mysymbols3[:50] #symbols[:100]
    #print("Top 100 Symbols:", top_100_symbols)

    dropped_coins = []
    dropped_coins1_5 = []
    increased_coins=[]
    increased_coins1_5=[]
    print("Veriler alınıyor....")
    for symbol in top_100_symbols:
        #if "USD_PERP" in symbol:
            try:
                klines = binanceclient.futures_klines(symbol=symbol.replace("USD_PERP", "USDT"), interval=Client.KLINE_INTERVAL_5MINUTE, limit=3)
                #open_prices = [float(kline[1]) for kline in klines]
                #0: Açılış zamanı
                #1: Açılış fiyatı
                #2: En yüksek fiyat
                #3: En düşük fiyat
                #4: Kapanış fiyatı
                #5: Hacim
                close_prices=[float(kline[4]) for kline in klines]
                if ((close_prices[0] - close_prices[-1]) / close_prices[0]) * 100 > 1:
                    dropped_coins.append(symbol.replace("USD_PERP", "USDT"))
                if ((close_prices[0] - close_prices[-1]) / close_prices[0]) * 100 > 1.5:
                    dropped_coins1_5.append(symbol.replace("USD_PERP", "USDT"))
                
                if ((close_prices[-1] - close_prices[0]) / close_prices[0]) * 100 > 1:
                    increased_coins.append(symbol.replace("USD_PERP", "USDT"))
                if ((close_prices[-1] - close_prices[0]) / close_prices[0]) * 100 > 1.5:
                    increased_coins1_5.append(symbol.replace("USD_PERP", "USDT"))
            except Exception as e:
                print(f"Error with symbol {symbol}: {str(e)}")
    print("🔻 dusenler_satis:",[dropped_coins, dropped_coins1_5])
    print("🔼 yükselenler alış:",[increased_coins, increased_coins1_5])
    return [dropped_coins, dropped_coins1_5, increased_coins,increased_coins1_5]



def short_pozisyonlari_tara():
    # Pozisyonları listele
    print("Açık pozisyonlar alınıyor...")
    positions = get_futures_positions()
    myshortlar=[]
    #karzarardurumu=[]
    #tsymbol=[]
    #tprice=[]
    #io49unaltinda=[]
    #mypozisyonlar=[]
    if positions:
        print("Short Pozisyonlar:")
        for pos in positions:
            print(pos)
            if pos["Position"]:
                if pos["Position"]<0:
            
                    #mypozisyonlar.append(binle(pos["Symbol"]))
                    print(binle(pos["Symbol"]))
                    myshortlar.append(binle(pos["Symbol"]))
        return myshortlar
                    

         
    else:
        print("Açık pozisyon bulunamadı.")

    
    
#import pygame


import subprocess



        


def AnaFonkSatis():
    global calissinmi
    calissinmi=False
    #mydusenler=dusenler_satis()
    top_50_symbols = mysymbols3[:10]
    mybtcyd=BTCdurumu()
    if mybtcyd[1]: #len(mydusenler[0])>4:
        for coin in top_50_symbols:

            if not coin in myshortlarGenel:
                sell_position(coin, 20, 1, "myshortlarGenel")
    elif not mybtcyd[1]: #len(mydusenler[0])<4:
        print("🔻🔻🔻🔻🔻SHORTLARIN HEPSİNİ KAPAAAAAATTTTTTT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        

        if not len(myshortlarGenel)==0:
            """
            # pygame mixer başlatma
            pygame.mixer.init()

            # Ses dosyasını yükleme
            sound = pygame.mixer.Sound('alarm2.wav')
            # Ses dosyasını çalma
            sound.play()

            # Ses bitene kadar bekletme
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
                time.sleep(1)

            # pygame kapatma (opsiyonel)
            pygame.quit()
            """
            

            # VLC ile dosyayı çalma
            subprocess.run([
                'am', 'start', '--user', '0',
                '-n', 'org.videolan.vlc/.gui.video.VideoPlayerActivity',
                '-d', 'file:///storage/emulated/0/Documents/alarm2.wav'
            ])

            for coin in myshortlarGenel:
                close_position(coin,"myshortlarGenel")
                time.sleep(1)
            myshortlarGenel.clear()
            #mylonglarGenel.clear()
             

            while False:
                kapatmismi=input("Shortları kapattın ise küçük harfle y yaz: ")
                if kapatmismi.lower()=="y":
                    myshortlarGenel.clear()
                    mylonglarGenel.clear()
                    break
                else:
                    print("çabuk kapat ve y yaz.")

    #Alış:
    if True:
        if mybtcyd[0]: #len(mydusenler[2])>4:
            for coin in top_50_symbols:

                if not coin in mylonglarGenel:
                    buy_position(coin, 20, 1, "mylonglarGenel")
        elif not mybtcyd[0]: #len(mydusenler[2])<4:
            print(" 🔼 🔼 🔼 🔼 BUYLARIN HEPSİNİ KAPAAAAAATTTTTTT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
            

            if not len(mylonglarGenel)==0:
                """
                # pygame mixer başlatma
                pygame.mixer.init()

                # Ses dosyasını yükleme
                sound = pygame.mixer.Sound('alarm2.wav')
                # Ses dosyasını çalma
                sound.play()

                # Ses bitene kadar bekletme
                while pygame.mixer.get_busy():
                    pygame.time.delay(100)
                    time.sleep(1)

                # pygame kapatma (opsiyonel)
                pygame.quit()
                """
                

                # VLC ile dosyayı çalma
                subprocess.run([
                    'am', 'start', '--user', '0',
                    '-n', 'org.videolan.vlc/.gui.video.VideoPlayerActivity',
                    '-d', 'file:///storage/emulated/0/Documents/alarm2.wav'
                ])
                
                for coin in mylonglarGenel:
                    close_position(coin,"mylonglarGenel")
                    time.sleep(1)
                mylonglarGenel.clear()
                #myshortlarGenel.clear()
                
                while False:
                    kapatmismi=input("Longları kapattın ise küçük harfle y yaz: ")
                    if kapatmismi.lower()=="y":
                        mylonglarGenel.clear()
                        myshortlarGenel.clear()
                        break
                    else:
                        print("çabuk kapat ve y yaz.")

        
    #else:
    #    if len(mydusenler[0])<1 and myshortlarGenel:
    #        mymyshortlar=short_pozisyonlari_tara()
    #        if mymyshortlar:
    #            for coin in mymyshortlar:
    #                close_position(coin,"myshortlarGenel")
    print("AnaFonkSatis işlemi tamamlandı.")
    calissinmi=True


################################# Ana Fonksiyon

while True:
    if calissinmi:
        AnaFonkSatis()
        time.sleep(5)
    else:
        time.sleep(5)