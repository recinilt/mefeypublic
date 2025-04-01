from telethon import TelegramClient, events
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


# Telegram Client'ı oluşturun
client = TelegramClient('session_name', api_id, api_hash)

def rastgele_sayi(min_deger, max_deger):
    return random.randint(min_deger, max_deger)

async def main():
    await client.start(phone=phone_number)

    @client.on(events.NewMessage(from_users=target_user))
    async def handler(event):
        print(f'Mesaj geldi: {event.raw_text}')
        pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
        matches = re.findall(pattern, event.raw_text, re.IGNORECASE)
        print(matches)
        modified_list = [s.replace(',', '.') for s in matches]
        float_list = [float(x) for x in modified_list]
        print(float_list)
         
        if any(number > kactanbuyuk for number in float_list):
            await client.send_message(alert_user, f"Listede {kactanbuyuk}'den büyük bir sayı bulundu! {event.raw_text}")
            print("bulundu")
    
    while True:
        await client.send_message(target_user, 'acc')
        await asyncio.sleep(rastgele_sayi(50, 300))  # 50 ile 300 saniye arasında rastgele bir saniyede bir mesaj gönder

with client:
    client.loop.run_until_complete(main())