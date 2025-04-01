import asyncio
from telethon import TelegramClient, events
import re

api_id = '21560699'  # Kendi API ID'nizi buraya girin
api_hash = '5737f22f317a7646f9be624a507984c6'  # Kendi API HASH'inizi buraya girin
phone = '+905056279048'  # Kendi telefon numaranızı buraya girin
message_interval = 180  # 3 dakikada bir mesaj gönderir
target_user = 'tradermikabot'  # Hedef kullanıcının kullanıcı adı
monitor_user = 'reccirik_bot'  # Cevapların kontrol edileceği kullanıcı adı
alert_user = 'reccirik_bot'  # Bildirim gönderilecek kullanıcı adı
message_text = 'acc'

client = TelegramClient(phone, api_id, api_hash)

async def send_message():
    while True:
        await client.send_message(target_user, message_text)
        await asyncio.sleep(message_interval)

async def handle_response(event):
    response = event.message.message
    pattern = r'\b\w+usdt\b(?:\s+\S+){1}\s+(\S+)'
    matches = re.findall(pattern, response, re.IGNORECASE)
    
    
    if any(num > 10.5 for num in matches):
        await client.send_message(alert_user, 'Bir sayı 10.5\'ten büyük!')

@client.on(events.NewMessage(from_users=monitor_user))
async def monitor(event):
    await handle_response(event)

async def main():
    await client.start()
    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.create_task(send_message())
loop.run_until_complete(main())