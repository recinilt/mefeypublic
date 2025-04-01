from telethon import TelegramClient, events
from binance.client import Client
import asyncio
import re
import random

# API ayarları
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'
target_user = 'tradermikabot'  # Hedef kullanıcının kullanıcı adı
alert_user = 'reccirik_bot'  # Bildirim gönderilecek kullanıcı adı
kactanbuyuk=17
binance_api="PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"
binance_secret="iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

#binance future listesi
binanceclient = Client(binance_api, binance_secret)
exchange_info = binanceclient.futures_exchange_info()
symbols = exchange_info['symbols']
print(symbols)
print(symbols[0]["symbol"])
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

accliler=[]


async def main():
    await client.start(phone=phone_number)

    @client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi: {event.raw_text}')
        #pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
        matches = re.findall(pattern, event.raw_text, re.IGNORECASE)
        print(matches)
        modified_list = [s.replace(',', '.') for s in matches]
        float_list = [float(x) for x in modified_list]
        print(float_list)
         
        #if any(number > kactanbuyuk for number in float_list):
        #    await client.send_message(alert_user, f"Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text}")
        #    print("bulundu")
        
        #pattern2 = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')
        matches2 = pattern2.findall(event.raw_text)
        result2 = [[match[0].replace(',', '.'), float(match[1].replace(',', '.')), float(match[2].replace(',', '.'))] for match in matches2]
        print(result2)
        print(result2[0][1])
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


        print("yes")
        #await client.send_message(alert_user, f"???Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text}")
    while True:
        await client.send_message(target_user, 'acc')
        await asyncio.sleep(rastgele_sayi(50, 300))  # 50 ile 300 saniye arasında rastgele bir saniyede bir mesaj gönder

with client:
    client.loop.run_until_complete(main())