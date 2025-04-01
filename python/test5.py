import asyncio
import re
from telethon import TelegramClient

# Telegram API Bilgileri
api_id = '21560699'
api_hash = '5737f22f317a7646f9be624a507984c6'
client = TelegramClient('session_name', api_id, api_hash)

# Mesaj İçerisindeki Sayıları Bulma Fonksiyonu
def extract_numbers(message):
    # usdt ile biten kelimelerden sonraki ikinci boşluktan sonraki sayıları bulma
    pattern = re.compile(r'\b\w+USDT\b.*?(\d+,\d+)')
    numbers = [float(num.replace(',', '.')) for num in pattern.findall(message)]
    return numbers

# Periyodik Mesaj Gönderme ve Kontrol Fonksiyonu
async def send_message_and_check():
    await client.start()

    while True:
        # Her 3 dakikada birine mesaj atma
        await client.send_message('tradermikabot', 'acc')
        
        # Gelen cevaptan sayıları çıkarma ve kontrol etme
        message = """
        VTHOUSDT 0,002343 11,2 2,87 0,17 + + + + + 1,89
        LTOUSDT 0,1760 10,5 1,32 0,15 + + + + + 2,53
        CTXCUSDT 0,3166 8,3 0,86 0,10 + + + + + 2,07
        LSKUSDT 1,047 6,8 0,34 0,04 + + + + + 1,19
        TNSRUSDT 0,5846 6,8 1,54 0,04 + + + - + 1,09
        AERGOUSDT 0,1228 6,3 1,41 0,02 + + + + + 1,32
        BTTCUSDT 0,00000112 5,6 0,81 0,01 + + + + + 1,03
        HBARUSDT 0,1330 5,5 0,30 0,06 - - + + + 1,94
        MAGICUSDT 0,4296 5,2 0,39 0,02 + + + + + 1,22
        DOGSUSDT 0,0006869 5,1 0,29 0,03 + - + + + 1,09
        ONGUSDT 0,3584 4,9 0,80 0,03 + + + + + 1,22
        ORDIUSDT 37,73 4,8 0,57 0,03 + + - - - 0,93
        GMTUSDT 0,1686 4,7 0,60 0,04 + + + + + 1,22
        MANAUSDT 0,4084 4,7 0,70 0,01 + + + + + 1,14
        NFPUSDT 0,2422 4,6 0,59 0,02 + - - - - 0,97
        """
        numbers = extract_numbers(message)
        if any(num > 10.5 for num in numbers):
            await client.send_message('other_receiver_username', 'There is a number greater than 10.5!')
        
        await asyncio.sleep(180)  # 3 dakika

asyncio.run(send_message_and_check())