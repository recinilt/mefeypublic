from telethon import TelegramClient, events
from binance.client import Client
import asyncio
import re
import random
import time
from binance.enums import *

# API ayarları
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'
target_user = 'tradermikabot'  # Hedef kullanıcının kullanıcı adı
alert_user = 'reccirik_bot'  # Bildirim gönderilecek kullanıcı adı
kactanbuyuk=17
binance_api="PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
binance_secret="iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"
mycost=1
myleverage=11
#binance future listesi
binanceclient = Client(binance_api, binance_secret)
exchange_info = binanceclient.futures_exchange_info()
symbols = exchange_info['symbols']
#print(symbols)
#print(symbols[0]["symbol"])
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s["symbol"])

def check_future_eligibility(symbol):
    for s in symbols:
        if s['symbol'] == symbol:
            return True
    return False

#symbol = 'BTCUSDT'  # Kontrol etmek istediğiniz sembolü girin
#is_eligible = check_future_eligibility(symbol)

#if is_eligible:
#    print(f"{symbol} future işlemleri için uygun.")
#else:
#    print(f"{symbol} future işlemleri için uygun değil.")


# Telegram Client'ı oluşturun
client = TelegramClient('session_name', api_id, api_hash)

def rastgele_sayi(min_deger, max_deger):
    return random.randint(min_deger, max_deger)

pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
pattern2 = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')
# Regex deseni 
#patternKA = r'\b(\w+)\s+TS:' 
# Eşleşmeleri bul 
#matches = re.findall(patternKA, text) # Eşleşmeleri yazdır print(matches)
# Regex deseni
patternKA = r'\b(\w+)\s+TS:'

# Eşleşmeleri bul
def get_price(symbol):
    try:
        ticker = binanceclient.get_symbol_ticker(symbol=symbol.upper())
        return ticker['price']
    except Exception as e:
        print(f"Error: {e}")
        return 1

def myquantity(coin):
    return round(((mycost*myleverage)/float(get_price(coin))),3)

#print(myquantity("pnutusdt"))

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


#close_position("pnutusdt")
'''
def open_position(coin):
    myq=myquantity(coin)
    ticker = binanceclient.get_symbol_info(symbol=coin) 
    precision = ticker['info']['pricePrecision'] 
    quantity = round(myq, precision)
    
    order = binanceclient.futures_create_order(
        symbol=coin,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
        leverage=myleverage
    )
    print(f"Pozisyon AÇILDI: {order}")
    time.sleep(10)  # 10 saniye bekle

open_position("PNUTUSDT")
'''

# Sembol bilgilerini alma
def get_symbol_precision(symbol):
    try:
        info = binanceclient.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol.upper():
                return int(item['quantityPrecision'])
    except Exception as e:
        print(f"Error: {e}")
        return None

# Pozisyon açma
def open_position(symbol, leverage, amount):
    try:
        binanceclient.futures_change_leverage(symbol=symbol, leverage=leverage)
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

#open_position("PNUTUSDT", myleverage, mycost)
#accliler=[]
KAliler=[]
print(f"merhaba {KAliler}")

async def main():
    await client.start(phone=phone_number)

    @client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi: {event.raw_text}')
        #pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
        #matches = re.findall(pattern, event.raw_text, re.IGNORECASE)
        #matches = re.findall(patternKA, text)
        #print(matches)
        #modified_list = [s.replace(',', '.') for s in matches]
        #float_list = [float(x) for x in modified_list]
        #print(float_list)
         
        #if any(number > kactanbuyuk for number in float_list):
        #    await client.send_message(alert_user, f"Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text}")
        #    print("bulundu")
        if event.raw_text.startswith("Canlı olan coin sayısı"):
            
            #pattern2 = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')
            matchesKA = re.findall(patternKA, event.raw_text)


            # Her bir eşleşmeye USDT ekleyip yeni bir liste oluştur
            usdt_listKA = [match + 'USDT' for match in matchesKA]
            myFKAlist=[]
            for coin in usdt_listKA:
                if coin in mysymbols3:
                    myFKAlist.append(coin)
            
            for coin in myFKAlist:
                if coin in KAliler:
                    print(f"{coin} zaten vardı")
                else:
                    KAliler.append(coin)
                    open_position(coin, myleverage, mycost)
                    print(f"{coin} long açıldı")
            
            for coin in KAliler:
                if coin in myFKAlist:
                    print(f"{coin} 'e zaten long açılmış.")
                else:
                    close_position(coin)
                    print(f"{coin} pozisyonu kapatıldı.")
                    KAliler.remove(coin)
            print(KAliler)
            #matches2 = pattern2.findall(event.raw_text)
            #result2 = [[match[0].replace(',', '.'), float(match[1].replace(',', '.')), float(match[2].replace(',', '.'))] for match in matches2]
            #print(result2)
            #print(result2[0][1])
            '''
            for satir in result2:
                if satir[1] >kactanbuyuk:
                    if satir[0] in mysymbols3: #check_future_eligibility(satir[0]):
                        await client.send_message(alert_user, f"Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text} \n {satir[0]} bulundu. acc:{satir[1]} Mts:{satir[2]}")
                        print(f"{satir[0]} bulundu. acc:{satir[1]} Mts:{satir[2]}")
                        if satir[0] in accliler:
                            print("zaten var")
                        else:
                            accliler.append(satir[0])
                            print(accliler)
                    else:
                        print("sembol yok")
                else:
                    print("büyük yok")
            '''

            #print(event.raw_text)
            print(myFKAlist)
            
        #await client.send_message(alert_user, f"???Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text}")
    while True:
        await client.send_message(target_user, 'ka')
        await asyncio.sleep(rastgele_sayi(100, 400))  # 100 ile 400 saniye arasında rastgele bir saniyede bir mesaj gönder

with client:
    client.loop.run_until_complete(main())