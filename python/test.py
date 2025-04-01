from telethon import TelegramClient, events
import asyncio

# API ayarları
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'

# Telegram Client'ı oluşturun
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)

    @client.on(events.NewMessage(from_users='tradermikabot'))
    async def handler(event):
        print(f'Mesaj geldi: {event.raw_text}')
        
    
    while True:
        await client.send_message('tradermikabot', 'acc')
        await asyncio.sleep(180)  # 3 dakikada bir mesaj gönder

with client:
    client.loop.run_until_complete(main())