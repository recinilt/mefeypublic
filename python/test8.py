from telethon import TelegramClient, events
import asyncio
import re
from telegram.ext import Updater, MessageHandler, Filters

# API ayarları
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
phone_number = '+905056279048'
target_user = 'tradermikabot'  # Hedef kullanıcının kullanıcı adı
alert_user = 'reccirik_bot'  # Bildirim gönderilecek kullanıcı adı


# Botunuzun token'ını buraya girin
TOKEN = '6754523785:AAFBKjgW3K_Wj3QIhe-mKzOtxRZwaLVPHOU'

def handle_message(update, context):
    message = update.message
    message.reply_text("Iyiyim.")
    print(message)
    #sender_id = message.from_user.id
    print("Gönderen ID:", sender_id)

# Telegram Client'ı oluşturun
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()
    
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
        
        
        
        if any(number > 10 for number in float_list):
            
            await client.send_message(alert_user, 'Listede 10.5\'ten büyük bir sayı bulundu!')
            print("bulundu")

    
    while True:
        await client.send_message(target_user, 'acc')
        await asyncio.sleep(203)  # 203 saniyede bir mesaj gönder

with client:
    client.loop.run_until_complete(main())