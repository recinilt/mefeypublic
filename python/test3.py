from telethon import TelegramClient, sync

# Telegram API bilgilerinizi buraya girin
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
phone = '+905056279048'
group_id = '@reccirik_bot'  # Mesaj göndermek istediğiniz grup ID'si

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Oturum aç
    await client.start(phone)

    # Kontrol etmek istediğiniz sayılar listesini oluşturun
    number_list = [8.0, 11.2, 7.5, 12.3, 9.8]

    # 10.5'ten büyük sayı varsa mesaj gönder
    if any(number > 10.5 for number in number_list):
        await client.send_message(group_id, 'Listede 10.5\'ten büyük bir sayı bulundu!')

    # Oturumu kapat
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())