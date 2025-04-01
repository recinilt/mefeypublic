import requests
import time
from binance.client import Client
from binance.enums import *
import pandas as pd

#testnet yapmak için, client oluştururken testnet=True yazmalı ve orderlarda test=True yazmalı.

binance_api_reccirik2="nKdNVSLZZo4hQnEI1rg7xU1cxZnPWHN4OePu8Yzc3wH3TptaLxBxwhBjUIjrFrAD"
binance_secret_reccirik2="WJSYPws6VnoJkMIXKqgu1CVSha9Io6rT7g8YEiNKbkG3dzdBF7vwZ6fWkZwvlH5S"

binanceclientreccirik2 = Client(binance_api_reccirik2, binance_secret_reccirik2)
mycost=1
myleverage=11
symbolstrailingprices=[]
mylonglar=[]
trailingyuzde=7
devammi=False
volumes=[]
myemavolumes=[]
mybtcprices=[]

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
        print(f"get_price() Error: {e}")
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
        print(f"get_symbol_precision() Error: {e}")
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
        print(f" buy_position() Error: {e}")

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
        print(f"sell_position Error: {e}")

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
        print(f"Bir hata oluştu: get_futures_position() {e}")
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


##############

def get_symbols():
    """Binance Futures API'den USDT bazlı coin çiftlerini alır."""
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [
        symbol["symbol"] for symbol in data["symbols"]
        if symbol["quoteAsset"] == "USDT" and symbol["contractType"] == "PERPETUAL"
    ]


def get_usdt_prices(symbol,interval,limit):
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params)
        data = response.json()
        #print(symbol, data)
        prices = [float(candle[4]) for candle in data]  # Kapanış fiyatlarını alır
        #print(prices)
        return prices
    except Exception as e:
        print(f"get_usdt_prices() Error: {e}")
        return [8,8,8,8,8,8,8,8]

# Fonksiyonu çağır ve fiyatları yazdır
#prices = get_btcusdt_prices()
#print(prices)
mysymbolsprices=[]
#get_BTCUSDT_historical_data("BTCUSDT","1h",2)
def get_historical_data(symbol, interval, limit):
    mysymbolsprices.append([symbol,get_usdt_prices(symbol,"5m",8)])
    """Her bir coin için tarihsel fiyat verilerini alır."""
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        return [{"close": float(candle[4]), "volume": float(candle[5])} for candle in data]
    return []

def calculate_increasing(liste): #ben ekledim
    coinpricecheck=[]
    for coin in liste:
        if coin[1][-1]>coin[1][-2] and coin[1][-2]>coin[1][-3]:# and coin[1][-3]>coin[1][-4] and coin[1][-4]>coin[1][-5] and coin[1][-5]>coin[1][-6] and coin[1][-6]>coin[1][-7]:
            coinpricecheck.append(coin[0])
    return coinpricecheck



def calculate_ema(data, period):
    """Bir veri serisinin EMA'sını hesaplar."""
    k = 2 / (period + 1)
    ema = [data[0]]  # İlk değer, serinin ilk kapanış fiyatıdır.
    for price in data[1:]:
        ema.append(price * k + ema[-1] * (1 - k))
    return ema


def analyze_ema(symbols, interval, short_ema_period, long_ema_period):
    """EMA kesişimlerini analiz eder."""
    ema_crosses = []
    for symbol in symbols:
        historical_data = get_historical_data(symbol, interval, long_ema_period + 5)
        #print(historical_data)
        
        myemavolumes.append([symbol,historical_data[-32]["volume"],historical_data[-31]["volume"],historical_data[-30]["volume"],historical_data[-29]["volume"],historical_data[-28]["volume"],historical_data[-27]["volume"],historical_data[-26]["volume"],historical_data[-25]["volume"],historical_data[-24]["volume"],historical_data[-23]["volume"],historical_data[-22]["volume"],historical_data[-21]["volume"],historical_data[-20]["volume"],historical_data[-19]["volume"],historical_data[-18]["volume"],historical_data[-17]["volume"],historical_data[-16]["volume"],historical_data[-15]["volume"],historical_data[-14]["volume"],historical_data[-13]["volume"],historical_data[-12]["volume"],historical_data[-11]["volume"],historical_data[-10]["volume"],historical_data[-9]["volume"],historical_data[-8]["volume"],historical_data[-7]["volume"],historical_data[-6]["volume"],historical_data[-5]["volume"],historical_data[-4]["volume"],historical_data[-3]["volume"],historical_data[-2]["volume"],historical_data[-1]["volume"]])
        volumes.append([symbol,historical_data[-1]["volume"]])
        if not historical_data:
            continue
        closes = [item["close"] for item in historical_data]
        short_ema = calculate_ema(closes, short_ema_period)
        long_ema = calculate_ema(closes, long_ema_period)
        #mybtcprices.append([symbol,historical_data[-2]["price"],historical_data[-1]["price"]])

        # Kesişim kontrolü
        if len(short_ema) >= 2 and len(long_ema) >= 2:
            if (short_ema[-1] > long_ema[-1] and short_ema[-2] <= long_ema[-2]):
                ema_crosses.append(symbol)
            elif (short_ema[-2] > long_ema[-2] and short_ema[-3] <= long_ema[-3]):
                ema_crosses.append(symbol)
            elif (short_ema[-3] > long_ema[-3] and short_ema[-4] <= long_ema[-4]):
                ema_crosses.append(symbol)
            elif (short_ema[-4] > long_ema[-4] and short_ema[-5] <= long_ema[-5]):
                ema_crosses.append(symbol)
    return ema_crosses


def listele():
    interval = "5m"  # Zaman dilimi
    short_ema_period = 12  # Kısa EMA periyodu
    long_ema_period = 100  # Uzun EMA periyodu

    print("USDT çiftleri yükleniyor...")
    symbols = get_symbols()
    print(f"{len(symbols)} çift bulundu. EMA analizi yapılıyor...")

    ema_crosses = analyze_ema(symbols, interval, short_ema_period, long_ema_period)
    
    print("EMA kesişimlerini yukarı kıran coin çiftleri:")
    ema_crosses_volume_right=[]
    #toplamvolume=sum(volumes)
    toplamvolume = sum(volume[1] for volume in volumes)
    for symbol in ema_crosses:
        for c in volumes:
            if c[0]==symbol:
                if (c[1]/toplamvolume)>0.0005:
                    ema_crosses_volume_right.append(symbol)
                    continue
        print(f"Yukarı kıran Sembol: {symbol}")
    if not ema_crosses:
        print("Kesişim yok.")
    print(f"Volumu yüksekler: {ema_crosses_volume_right}")
    volumeemasiyuksekolanlar=find_my_volume_ema_high(myemavolumes)
    kesisim= list(set(ema_crosses_volume_right) & set(volumeemasiyuksekolanlar))
    print(f"yukarı kıran ve volümü yükselen: {kesisim}")
    myemavolumes.clear()
    volumes.clear()

    increasingcheck=calculate_increasing(mysymbolsprices)
    mysymbolsprices.clear()
    kesisimpriceincreasing=list(set(increasingcheck) & set(ema_crosses_volume_right))
    return kesisimpriceincreasing
    #return(kesisim)
    #mybtcprices.append(get_btcusdt_prices())
    #if mybtcprices[0][1]>mybtcprices[0][0]:
    #    mybtcprices.clear()
    #    return ema_crosses_volume_right
    #else:
    #    mybtcprices.clear()
    #    return []

#if __name__ == "__main__":
#    main()
devammi=True
while True:
    if devammi:
        print("emakesisim12-50 v2.py")
        longacilacaksymbols=listele()
        print(f"Long açılacak coinler: {longacilacaksymbols}")
        for coin in longacilacaksymbols:
            if coin in mylonglar:
                print(f"{coin} zaten vardı")
            else:
                #mylonglarKA.append(coin)
                buy_position(coin, myleverage, mycost)
                #print(f"{coin} long açıldı")

        for i in range(6):
            positions = get_futures_positions()
            kapatılacaklar=[]
            karzarardurumu=[]
            tsymbol=[]
            tprice=[]
            io49unaltinda=[]
            if positions:
                print("Açık Pozisyonlar:")
                for pos in positions:
                    print(pos)
                    if pos["P&L (%)"]>(200) or pos["P&L (%)"]<(-1*trailingyuzde):
                        kapatılacaklar.append([pos["Symbol"],pos["Mark Price"]])
                    kar=pos["Position"]*pos["Entry Price"]*pos['P&L (%)']*0.01
                    #print(kar)
                    karzarardurumu.append(kar)
                    tsymbol.append(pos["Symbol"])
                    #if io1d[-1]<49:
                    #    io49unaltinda.append(pos["Symbol"])
                    myp=get_price(pos["Symbol"])
                    tprice.append(myp)
                    symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (pos["Symbol"],myp))
                print(f"şuan açık pozisyonların toplam kar zarar durumu: {sum(karzarardurumu)} USDT")
            else:
                print("Açık pozisyon bulunamadı.")


            for c in kapatılacaklar:
                #mymesaj.append(c[0])
                close_position(c[0])
                symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (c[0],c[1]),True)
                time.sleep(8)
            
            trailing_dusen_coinler = fiyat_dalgalanma_takip(symbolstrailingprices, trailingyuzde)
            print(f" trailing düşen coinler: {trailing_dusen_coinler}")
            if trailing_dusen_coinler:
                #telegram_client.send_message(alert_user, f"{trailing_dusen_coinler} trailing stop ile kapatılan coinler.")
                for coin in trailing_dusen_coinler:
                    close_position(coin)
                    #mymesaj.append(coin)
                    symbolstrailingprices = fiyat_guncelle(symbolstrailingprices, (coin,0.0000000001),True)
                    time.sleep(8)
            time.sleep(15)
        
        time.sleep(5)
    else:
        time.sleep(10)
    

    

    

