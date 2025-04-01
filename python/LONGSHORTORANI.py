import requests
import json

# Binance API üzerinden Top Trader Long/Short Ratio verisini çekmek için kullanılan fonksiyon
def get_top_trader_long_short_ratio(symbol='LDOUSDT'):
    try:
        url = f'https://fapi.binance.com/futures/data/topLongShortPositionRatio'
        
        # Parametreler
        params = {
            'symbol': symbol,         # İlgili işlem çifti
            'period': '15m',            # Zaman dilimi: 5 dakikalık
            'limit': 30               # Sonuç sayısı: Son 30 veri
        }
        
        # API isteği yapıyoruz
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Yanıtı yazdırarak yapıyı inceleyelim
            print("API Yanıtı:", json.dumps(data, indent=4))  # Veriyi düzgün bir şekilde yazdır

            # Veriyi işleyelim
            for entry in data:
                # Yanıtın içinde 'longShortRatio' ve diğer alanların mevcut olup olmadığını kontrol ediyoruz
                print(f"Date: {entry.get('timestamp')}")
                print(f"Long/Short Ratio: {entry.get('longShortRatio')}")
                print(f"Long Position: {entry.get('longPosition')}")
                print(f"Short Position: {entry.get('shortPosition')}")
                print('-' * 50)
        else:
            print(f"API hatası: {response.status_code}")
    
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Veri çekme ve yazdırma
get_top_trader_long_short_ratio(symbol='LDOUSDT')
