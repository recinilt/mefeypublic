import requests
import requests
import time
from binance.client import Client
from binance.enums import *
import pandas as pd



binance_api_reccirik2="nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_reccirik2="WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"

binanceclientreccirik2 = Client(binance_api_reccirik2, binance_secret_reccirik2)
mycost=1
myleverage=11
symbolstrailingprices=[]
mylonglar=[]
trailingyuzde=1
devammi=False
volumes=[]
myemavolumes=[]


################### myema
# Verilen liste
data = [
    ["BTCUSDT", 2.1, 2.2, 2.3, 2.2, 2.2, 2.2, 2.4, 2.5, 2.4],
    ["LTCUSDT", 2.1, 2.2, 2.3, 2.2, 2.2, 2.2, 2.4, 2.5, 2.4],
    ["XRPUSDT", 2.1, 2.2, 2.3, 2.2, 2.2, 2.2, 2.4, 2.5, 2.4],
    ["UNIUSDT", 2.9, 2.2, 2.3, 2.4, 2.2, 2.2, 2.1, 2.2, 2.0],
]

# EMA hesaplama fonksiyonu
def calculate_my_ema(values, period):
    return pd.Series(values).ewm(span=period, adjust=False).mean().tolist()

# EMA'yı yukarı kıranları bulma
def find_my_volume_ema_high(data):
    volumesiyukseliyor = []
    for row in data:
        coin = row[0]
        volumes = row[1:]
        ema2 = calculate_ema(volumes, 2)
        ema3 = calculate_ema(volumes, 9)
        
        # EMA'nın yukarı kırıldığı anları kontrol et
        for i in range(1, len(volumes)):
            if ema2[i] > ema3[i]: #and ema2[i-1] <= ema3[i-1]:
                volumesiyukseliyor.append(coin)
                break  # Bir kez yukarı kırılması yeterli
    #print(f"volumesi yükseliyor: {volumesiyukseliyor}")
    return volumesiyukseliyor

# Yukarı kıranları bul
#myresult = find_my_ema_cross(myemavolumes)
#print("EMA'yı yukarı kıranlar:", result)

####################
def get_price(symbol):
    try:
        ticker = binanceclientreccirik2.get_symbol_ticker(symbol=symbol.upper())
        return ticker['price']
    except Exception as e:
        print(f"Error: {e}")
        return 1

def myquantity(coin):
    return round(((mycost*myleverage)/float(get_price(coin))),3)

def close_position(coin):
    # Mevcut pozisyonu kapat
    positions = binanceclientreccirik2.futures_position_information(symbol=coin)
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            myquantity=abs(float(position['positionAmt']))
            #karzararesapla(coin,myquantity,position['entryPrice'],get_price(coin),liste,1 if side=="SIDE_BUY" else -1)
            order = binanceclientreccirik2.futures_create_order(
                symbol=coin,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=myquantity
            )
            print(f"Pozisyon kapatıldı: {order}")
            mtext=f"Kapatılan Çift: {position['symbol']}, Miktar: {position['positionAmt']}, Giriş Fiyatı: {position['entryPrice']}, Çıkış fiyatı: {get_price(position["symbol"])}"
            #acmakapamalistesi.append(mtext)
            print(mtext)
            if position["symbol"] in mylonglar:
                mylonglar.remove(position["symbol"])
            #hesapla(coin, side, myquantity)
            #eklesil(coin,liste,"sil")
            time.sleep(5)  # 5 saniye bekle
    # Futures cüzdanındaki USDT miktarını öğren
    #account_info = binanceclient.futures_account()  # Futures hesap bilgilerini al
    #usdt_balance = 0

def get_symbol_precision(symbol):
    try:
        info = binanceclientreccirik2.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol.upper():
                return int(item['quantityPrecision'])
    except Exception as e:
        print(f"Error: {e}")
        return None

def buy_position(symbol, leverage, amount):
    #if is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
    try:
        binanceclientreccirik2.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclientreccirik2.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        
        order = binanceclientreccirik2.futures_create_order(
            symbol=symbol.upper(),
            side='BUY',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        print(order)
        if not coin in mylonglar:
            mylonglar.append(coin)
        #hesapla(symbol, "buy",1)
        #eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")

def sell_position(symbol, leverage, amount):
    #•if not is_above_last_period_average(io1d[len(io1d)-1],io1d,smaperiod):
    try:
        binanceclientreccirik2.futures_change_leverage(symbol=symbol, leverage=leverage)
        #binanceclient.futures_change_margin_type(symbol=symbol, marginType=ISOLATED)
        precision = get_symbol_precision(symbol)
        if precision is None:
            print("Precision could not be determined.")
            return

        quantity = round(amount * leverage / float(binanceclientreccirik2.get_symbol_ticker(symbol=symbol.upper())['price']), precision)
        
        order = binanceclientreccirik2.futures_create_order(
            symbol=symbol.upper(),
            side='SELL',
            type='MARKET',
            quantity=quantity,
            leverage=leverage
        )
        print(order)
        #hesapla(symbol,"sell",1)
        #eklesil(symbol,liste,"ekle")
        time.sleep(5)  # 5 saniye bekle
    except Exception as e:
        print(f"Error: {e}")

def acabilirmiyim(coin):
    if coin in mylonglar:#mylonglarSDV or coin in mylonglarCi or coin in mylonglarKA or coin in mylonglarMA or coin in mylonglarIOF or coin in myshortlarCi or coin in myshortlarIOF or coin in myshortlarSDV:
        return False
    else:
        return True 

##
def get_futures_positions():
    try:
        # Binance Futures account position endpoint
        account_info = binanceclientreccirik2.futures_account()
        positions = account_info['positions']

        result = []
        for position in positions:
            # Sadece açık pozisyonları kontrol et (pozisyon miktarı 0'dan farklı olmalı)
            if float(position['positionAmt']) != 0:
                symbol = position['symbol']
                position_amt = float(position['positionAmt'])
                entry_price = float(position['entryPrice'])
                #mark_price = float(position['markPrice'])
                mark_price=float(get_price(symbol))
                leverage = int(position['leverage'])

                # P&L hesaplama
                pnl = (mark_price - entry_price) / entry_price * 100 * (1 if position_amt > 0 else -1)
                result.append({
                    'Symbol': symbol,
                    'Position': position_amt,
                    'Entry Price': entry_price,
                    'Mark Price': mark_price,
                    'Leverage': leverage,
                    'P&L (%)': round(pnl, 2)
                })

        return result

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []

# Pozisyonları listele
positions = get_futures_positions()
print(positions)
if positions:
    print("Açık Pozisyonlar:")
    for pos in positions:
        print(pos)
else:
    print("Açık pozisyon bulunamadı.")
##
def fiyat_kontrolu(yuzde, fiyat_listesi):
    # En yüksek fiyatı bul
    en_yuksek_fiyat = float(max(fiyat_listesi))
    
    # En son eklenen fiyatı al
    son_eklenen_fiyat = float(fiyat_listesi[-1])
    
    # Yüzde olarak düşüş miktarını hesapla
    yuzde_fiyat_dususu = en_yuksek_fiyat * (float(yuzde) / 100)
    
    # Son eklenen fiyat, en yüksek fiyatın %yüzde kadar altındaysa True döndür
    if en_yuksek_fiyat - son_eklenen_fiyat >= yuzde_fiyat_dususu:
        return True
    else:
        return False


def fiyat_guncelle(kripto_listesi, yeni_veri, sil=False):
    # yeni_veri: ("BTCUSDT", 50000) gibi bir tuple
    kripto_cifti, fiyat = yeni_veri
    
    # Kripto çiftinin listede olup olmadığını kontrol et
    for kripto in kripto_listesi:
        if kripto[0] == kripto_cifti:
            if sil:
                # Kripto çiftini ve fiyat bilgilerini sil
                kripto_listesi.remove(kripto)
            else:
                # Kripto çifti bulundu, yeni fiyatı float olarak ekle
                kripto[1].append(float(fiyat))
            return kripto_listesi
    
    # Kripto çifti listede yoksa ve silme işlemi yapılmıyorsa, yeni bir eleman ekle
    if not sil:
        kripto_listesi.append([kripto_cifti, [float(fiyat)]])
    return kripto_listesi
"""
# Örnek kullanım
kripto_listesi = [
    ["BTCUSDT", [48000.0, 49000.0]],
    ["ETHUSDT", [1500.0, 1600.0]]
]

# Yeni fiyat ekleme
yeni_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Yeni kripto çifti ekleme
yeni_veri = ("XRPUSDT", 1.2)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Kripto çifti ve fiyat bilgilerini silme
sil_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, sil_veri, sil=True)
print(kripto_listesi)
   
    
    # yeni_veri: ("BTCUSDT", 50000) gibi bir tuple
    kripto_cifti, fiyat = yeni_veri
    
    # Kripto çiftinin listede olup olmadığını kontrol et
    for kripto in kripto_listesi:
        if kripto[0] == kripto_cifti:
            if sil:
                # Kripto çiftini ve fiyat bilgilerini sil
                kripto_listesi.remove(kripto)
            else:
                # Kripto çifti bulundu, yeni fiyatı ekle
                kripto[1].append(fiyat)
            return kripto_listesi
    
    # Kripto çifti listede yoksa ve silme işlemi yapılmıyorsa, yeni bir eleman ekle
    if not sil:
        kripto_listesi.append([kripto_cifti, [fiyat]])
    return kripto_listesi

# Örnek kullanım
kripto_listesi = [
    ["BTCUSDT", [48000, 49000]],
    ["ETHUSDT", [1500, 1600]]
]

# Yeni fiyat ekleme
yeni_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Yeni kripto çifti ekleme
yeni_veri = ("XRPUSDT", 1.2)
kripto_listesi = fiyat_guncelle(kripto_listesi, yeni_veri)
print(kripto_listesi)

# Kripto çifti ve fiyat bilgilerini silme
sil_veri = ("BTCUSDT", 50000)
kripto_listesi = fiyat_guncelle(kripto_listesi, sil_veri, sil=True)
print(kripto_listesi)
"""

def fiyat_dalgalanma_takip(symbols_trailing_prices, yuzde):
    dusen_coinler = []
    for coin in symbols_trailing_prices:
        symbol, prices = coin
        max_fiyat = max(prices)
        son_fiyat = prices[-1]
        if (max_fiyat - son_fiyat) / max_fiyat * 100 > yuzde:
            dusen_coinler.append(symbol)
    return dusen_coinler


##################################
def fetch_futures_data(threshold=2.5):
    try:
        # Binance USDT Futures çiftlerini al
        exchange_info_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        exchange_info = requests.get(exchange_info_url).json()
        usdt_pairs = [pair['symbol'] for pair in exchange_info['symbols'] if pair['quoteAsset'] == 'USDT' and pair['status'] == 'TRADING']

        found_pairs = []

        for pair in usdt_pairs:
            try:
                # Her bir paritenin son iki periyodundaki 1 dakikalık kline verilerini al
                klines_url = f'https://fapi.binance.com/fapi/v1/klines?symbol={pair}&interval=1m&limit=2'
                klines = requests.get(klines_url).json()

                if len(klines) == 2:
                    open_price = float(klines[0][1])  # İlk periyodun açılış fiyatı
                    close_price = float(klines[1][4])  # İkinci periyodun kapanış fiyatı
                    percentage_change = ((close_price - open_price) / open_price) * 100

                    if percentage_change >= threshold:
                        found_pairs.append(f"{pair} (%{percentage_change:.2f})")
            except Exception as e:
                print(f"Veri alınırken hata oluştu: {pair}, {str(e)}")
                continue

        return found_pairs

    except Exception as e:
        print(f"Genel bir hata oluştu: {str(e)}")
        return []
##################################################
# Kullanım
if __name__ == "__main__":
    threshold = 2.5  # Yüzde eşiği
    results = fetch_futures_data(threshold)
    if results:
        print(f"Son 2 periyotta %{threshold} veya üzeri yükselen pariteler:")
        for result in results:
            print(result)
    else:
        print(f"Son 2 periyotta %{threshold} veya üzeri yükselen bir parite bulunamadı.")
    print("emakesisim12-50 v3")
