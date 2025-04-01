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
binance_api_MMA="tVhTcbB2PaqBx8kaRyI5Eaw0hV6zvcNf0YNjG6Ah4AgFqiHddW49zaZwwOdQmagN"
binance_secret_MMA="A0QffERd8Qg4QBlOsRgjxGQOn5Ajdch9vyYsneL2V8xf3j9kcSKUjMU0fNCLfJAz"


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
mylonglarSSR=[]
mylonglarOB=[]
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
#ilkkackez=int(input("kaç tane io eklensin?"))
for i in range(1, 20):
    #print(i)
    io1d.append(ilkio)
cirawtext=[]
acmakapamalistesi=[]
usdtlistem=[]
iopower=[1]
yasaklilist=["ETHUSDT","SOLUSDT","BTCUSDT","USDCUSDT","CTKUSDT"]
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
tumcoinlerinalimsatimorani=[1]
mymesaj=["naber"]

soracaklarim=["Hangi coin?", "alt sınır?", "üst sınır?", "kaç grid olsun?"]

def myanafonk():
    mytext="""
    merhaba
    naber
    nasılsın
    iyi misin?
    """
    return mytext
##################################### Yardımcı Fonksiyonlar:

async def mesajgonder(mesaj,alici):
    await telegram_client.send_message(alici, mesaj)

################################# Ana Fonksiyon

async def main():
    global iokomutlari
    global iocoins
    global apalayimmi
    global apsatayimmi
    global apkisaalayimmi
    global apuzunalayimmi
    global calissinmi
    global io1d
    await telegram_client.start(phone=phone_number)
    @telegram_client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi:\n {event.raw_text}')
        global iocoins
        global calissinmi
        global apalayimmi
        global apsatayimmi
        global apkisaalayimmi
        global apuzunalayimmi
        global iokomutlari
        global io1d

        if event.raw_text.startswith("Marketteki Tüm Coinlere Olan Nakit Girişi Raporu"): #IO
            while True:
                if calissinmi:
                    AnaFonkIO(event.raw_text)
                    print("io")
                    if io1d[-1]<49:
                        #AnaFonkSatis()
                        print("AnaFonkSatis()")
                    break
                else:
                    await asyncio.sleep(5)

            print("ls")
        elif "karakterli alarm eklenme durumu" in event.raw_text:
            print("nls")
        elif "TrendLevels_Big:" in event.raw_text:
            print("sr coin")
        else:
            ozelmesaj.append(event.raw_text)

    while True:
        if True:
            
            if mymesaj:
                for mesaj in mymesaj:
                    await mesajgonder(f"Otomatik kapatılan coinler: {mesaj}",alert_user)
                mymesaj.clear()
            if ozelmesaj:
                for mesaj in ozelmesaj:
                    await mesajgonder(f"Özel Mesajınız Var: \n{mesaj}",alert_user)
                ozelmesaj.clear()
            
            await telegram_client.send_message(target_user, "ap")
            await asyncio.sleep(2*rastgele_sayi(15,45))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
            while True:
                if calissinmi:
                    await telegram_client.send_message(target_user, "io")
                    await asyncio.sleep(2*rastgele_sayi(30,45))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder
                    break
                else:
                    await asyncio.sleep(2)
            
        

with telegram_client:
    telegram_client.loop.run_until_complete(main())